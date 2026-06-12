#!/usr/bin/env python3
"""
h3_gate2_backtest_v1.0.0.py
===========================
H3 month-end FX rebalancing flow - GATE 2, IN-SAMPLE ONLY (exit <= 2017-12-31).
Locked rules per H3_MonthEnd_Gate1_Spec_v1.0.0.md. No optimisation. No OOS peek.

Run from repo root (needs fx_data/ and index_data/).
"""

import csv, math, bisect
from datetime import date

IN_SAMPLE_END = date(2017, 12, 31)
N_OFFSET = 5  # entry = LTD index - 5

# pair -> (home index, base_sign). base_sign +1 foreign BASE, -1 foreign QUOTE.
CORE = {
    "EURUSD": ("EU50_EUR",  +1),
    "GBPUSD": ("UK100_GBP", +1),
    "AUDUSD": ("AU200_AUD", +1),
    "USDCHF": ("CH20_CHF",  -1),
}
SATELLITE = {"USDJPY": ("JP225Y_JPY", -1)}
BENCH = "SPX500_USD"

# --------------------------------------------------------------------------

def load_series(path):
    """Mon-Fri only. Returns list of (date, c_mid) sorted ascending."""
    out = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            d = date.fromisoformat(r["date"])
            if d.weekday() >= 5:   # drop Sat/Sun partials
                continue
            out.append((d, float(r["c_mid"])))
    out.sort(key=lambda x: x[0])
    return out

def asof(series_dates, series_vals, target):
    """Index close on-or-before target (forward-fill, no look-ahead)."""
    i = bisect.bisect_right(series_dates, target) - 1
    if i < 0:
        return None
    return series_vals[i]

def month_key(d):
    return (d.year, d.month)

def build_months(fx):
    """Return list of dicts: month_start_idx, entry_idx, ltd_idx (global indices)."""
    groups = {}
    order = []
    for i, (d, _) in enumerate(fx):
        k = month_key(d)
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(i)
    trades = []
    for k in order:
        idxs = groups[k]
        ms_idx = idxs[0]
        ltd_idx = idxs[-1]
        entry_idx = ltd_idx - N_OFFSET
        if entry_idx <= ms_idx:
            continue
        if month_key(fx[entry_idx][0]) != k:
            continue
        trades.append({"ms": ms_idx, "entry": entry_idx, "ltd": ltd_idx})
    return trades

def run_pair(pair, home_name, base_sign, fx_dir="fx_data", ix_dir="index_data"):
    fx = load_series(f"{fx_dir}/{pair}_daily.csv")
    home = load_series(f"{ix_dir}/{home_name}_daily.csv")
    spx = load_series(f"{ix_dir}/{BENCH}_daily.csv")
    hd = [d for d, _ in home]; hv = [v for _, v in home]
    sd = [d for d, _ in spx];  sv = [v for _, v in spx]

    rows = []
    for t in build_months(fx):
        ms_date = fx[t["ms"]][0]
        entry_date, entry_mid = fx[t["entry"]]
        ltd_date, exit_mid = fx[t["ltd"]]

        h0 = asof(hd, hv, ms_date); h1 = asof(hd, hv, entry_date)
        s0 = asof(sd, sv, ms_date); s1 = asof(sd, sv, entry_date)
        if None in (h0, h1, s0, s1):
            continue
        r_home = math.log(h1 / h0)
        r_spx = math.log(s1 / s0)
        diff = r_home - r_spx
        if diff == 0:
            continue
        s = 1 if diff > 0 else -1
        dirn = -s * base_sign
        ret_bps = dirn * math.log(exit_mid / entry_mid) * 10000.0

        rows.append({
            "pair": pair, "ms": ms_date, "entry": entry_date, "exit": ltd_date,
            "s": s, "dir": dirn, "ret_bps": ret_bps,
            "hold_days": t["ltd"] - t["entry"],
        })
    return rows, fx

def stats(rets):
    n = len(rets)
    if n == 0:
        return None
    mean = sum(rets) / n
    if n > 1:
        var = sum((x - mean) ** 2 for x in rets) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0
    t = (mean / (std / math.sqrt(n))) if std > 0 else float("nan")
    wins = sum(1 for x in rets if x > 0)
    win_rate = wins / n
    gross_win = sum(x for x in rets if x > 0)
    gross_loss = -sum(x for x in rets if x < 0)
    pf = (gross_win / gross_loss) if gross_loss > 0 else float("inf")
    cum = 0.0; peak = 0.0; mdd = 0.0
    for x in rets:
        cum += x
        peak = max(peak, cum)
        mdd = min(mdd, cum - peak)
    return {"n": n, "mean": mean, "std": std, "t": t, "win": win_rate,
            "pf": pf, "mdd": mdd, "worst": min(rets), "best": max(rets),
            "total": sum(rets)}

def winsorise(vals, lo=1, hi=99):
    s = sorted(vals)
    n = len(s)
    def pct(p):
        k = (n - 1) * p / 100.0
        f = math.floor(k); c = math.ceil(k)
        if f == c: return s[int(k)]
        return s[f] * (c - k) + s[c] * (k - f)
    lob, hib = pct(lo), pct(hi)
    return [min(max(x, lob), hib) for x in vals], lob, hib

def fmt(st, label):
    if st is None:
        return f"  {label:<14} no trades"
    return (f"  {label:<14} n={st['n']:>4}  mean={st['mean']:>8.2f}bps  "
            f"t={st['t']:>6.2f}  win={st['win']*100:>5.1f}%  PF={st['pf']:>5.2f}  "
            f"MDD={st['mdd']:>9.1f}  worst={st['worst']:>9.1f}  tot={st['total']:>10.1f}")

# --------------------------------------------------------------------------

def main():
    print("=" * 96)
    print("H3 GATE 2 - IN-SAMPLE BACKTEST (exit <= 2017-12-31).  Locked spec. No optimisation.")
    print("=" * 96)

    core_all = []
    per_pair_is = {}
    total_is_trading_days = None

    for pair, (home, bsign) in CORE.items():
        rows, fx = run_pair(pair, home, bsign)
        is_rows = [r for r in rows if r["exit"] <= IN_SAMPLE_END]
        per_pair_is[pair] = is_rows
        core_all.extend(is_rows)
        if total_is_trading_days is None:
            total_is_trading_days = sum(1 for d, _ in fx if d <= IN_SAMPLE_END)

    print("\nPER-PAIR (in-sample):")
    sign_pos = 0
    for pair in CORE:
        rets = [r["ret_bps"] for r in per_pair_is[pair]]
        st = stats(rets)
        print(fmt(st, pair))
        if st and st["mean"] > 0:
            sign_pos += 1

    print(f"\nPER-PAIR SIGN CONSISTENCY: {sign_pos}/4 pairs positive mean.")

    pooled = [r["ret_bps"] for r in core_all]
    st_raw = stats(pooled)
    print("\nPOOLED CORE-4 (raw):")
    print(fmt(st_raw, "CORE-4 raw"))

    wvals, lob, hib = winsorise(pooled, 1, 99)
    st_w = stats(wvals)
    print(f"\nPOOLED CORE-4 (winsorised 1/99 pct: clip to [{lob:.1f}, {hib:.1f}] bps):")
    print(fmt(st_w, "CORE-4 wins"))

    avg_hold = sum(r["hold_days"] for r in core_all) / len(core_all)
    tim = (len(core_all) * avg_hold) / (total_is_trading_days * 4)
    print(f"\nHOLD/EXPOSURE: avg hold = {avg_hold:.2f} trading days | "
          f"time-in-market ~ {tim*100:.1f}% of available pair-days "
          f"(in-sample trading days/pair = {total_is_trading_days}).")

    print("\nSNB 2015-01 USDCHF trade (shown, not dropped):")
    for r in per_pair_is["USDCHF"]:
        if r["exit"].year == 2015 and r["exit"].month == 1:
            print(f"  entry {r['entry']} -> exit {r['exit']} | s={r['s']} dir={r['dir']} "
                  f"ret={r['ret_bps']:.1f}bps")

    sat_rows, _ = run_pair("USDJPY", *SATELLITE["USDJPY"])
    sat_is = [r for r in sat_rows if r["exit"] <= IN_SAMPLE_END]
    print(f"\nSATELLITE USDJPY: in-sample trades = {len(sat_is)} "
          f"(JP225Y index starts 2020-04-27 -> none <=2017). Parked for Gate 3.")

    print("\n" + "=" * 96)
    return st_raw, st_w, sign_pos, core_all

if __name__ == "__main__":
    main()
