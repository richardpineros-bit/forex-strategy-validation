#!/usr/bin/env python3
"""
h4_gate2_backtest_v1.0.0.py — H4 cross-sectional currency momentum, Gate 2.
IN-SAMPLE ONLY: 2005-01-02 .. 2017-12-31. OOS (2018+) is SEALED — never loaded here.
Implements H4_XSecMomentum_Gate1_Spec_v1.0.0 exactly. Pure stdlib (no pandas).

Spec realisation:
- Normalise to USD-per-foreign: invert USD-base pairs, foreign-base used direct.
- Monthly series = last trading day of each calendar month (normalised close).
- Signal at month-end t = trailing 3-month return = norm[t]/norm[t-3] - 1.
- Rank 9 desc; LONG top-3, SHORT bottom-3, equal weight; dollar-neutral.
- Forward (held) return per name = norm[t+1]/norm[t] - 1 (spot, month-end to month-end).
- Monthly L-S spread = mean(top3 fwd) - mean(bottom3 fwd).
"""
import csv, math
from datetime import datetime

IS_START="2005-01-02"; IS_END="2017-12-31"
FOREIGN_BASE={"EURUSD","GBPUSD","AUDUSD","NZDUSD"}      # use c_mid direct
USD_BASE={"USDCHF","USDJPY","USDCAD","USDSEK","USDNOK"} # invert 1/c_mid
NAMES=["EURUSD","GBPUSD","AUDUSD","USDCHF","USDJPY","NZDUSD","USDCAD","USDSEK","USDNOK"]
L=3  # month-ends lookback
K=3  # legs

def load_norm(name):
    """Return dict date->normalised close (USD-per-foreign), IS window only."""
    out={}
    with open(f"fx_data/{name}_daily.csv") as f:
        for row in csv.DictReader(f):
            d=row["date"].strip()
            if d<IS_START or d>IS_END: continue
            mid=float(row["c_mid"])
            out[d]= (1.0/mid) if name in USD_BASE else mid
    return out

def month_end_series(daily):
    """Collapse daily dict to last-trading-day-of-month: list of (ym, date, value)."""
    by_month={}
    for d in sorted(daily):
        ym=d[:7]
        by_month[ym]=d  # last seen wins (dates sorted asc) => last trading day
    return [(ym, by_month[ym], daily[by_month[ym]]) for ym in sorted(by_month)]

# Build aligned monthly panel
series={n: month_end_series(load_norm(n)) for n in NAMES}
months=sorted(set.intersection(*[{ym for ym,_,_ in series[n]} for n in NAMES]))
val={n:{ym:v for ym,_,v in series[n]} for n in NAMES}

spreads=[]; longs=[]; shorts=[]; rows=[]
for i in range(L, len(months)-1):
    t=months[i]; t_prev=months[i-L]; t_next=months[i+1]
    sig={n: val[n][t]/val[n][t_prev]-1.0 for n in NAMES}          # 3m trailing
    fwd={n: val[n][t_next]/val[n][t]-1.0 for n in NAMES}          # held next month
    ranked=sorted(NAMES, key=lambda n: sig[n], reverse=True)
    top=ranked[:K]; bot=ranked[-K:]
    lret=sum(fwd[n] for n in top)/K
    sret=sum(fwd[n] for n in bot)/K
    ls=lret-sret
    spreads.append(ls); longs.append(lret); shorts.append(sret)
    rows.append((t,t_next,top,bot,lret,sret,ls))

# ---- stats ----
n=len(spreads)
mean=sum(spreads)/n
var=sum((x-mean)**2 for x in spreads)/(n-1)
sd=math.sqrt(var)
tstat=mean/(sd/math.sqrt(n))
winrate=100.0*sum(1 for x in spreads if x>0)/n
gains=sum(x for x in spreads if x>0); losses=-sum(x for x in spreads if x<0)
pf=gains/losses if losses>0 else float('inf')
lmean=sum(longs)/n; smean=sum(shorts)/n
ann=mean*12*100; sharpe=(mean/sd)*math.sqrt(12)
# max drawdown on compounded equity
eq=1.0; peak=1.0; mdd=0.0
for x in spreads:
    eq*=(1+x); peak=max(peak,eq); mdd=min(mdd,eq/peak-1)

print("="*64)
print("H4 GATE 2 — CROSS-SECTIONAL CURRENCY MOMENTUM (IN-SAMPLE)")
print("Window: %s .. %s   |  OOS 2018+ SEALED (not loaded)"%(IS_START,IS_END))
print("="*64)
print(f"Aligned month-ends     : {len(months)}  ({months[0]} .. {months[-1]})")
print(f"L-S observations (n)   : {n}")
print(f"First held month       : {rows[0][1]}   Last held: {rows[-1][1]}")
print("-"*64)
print(f"Mean monthly L-S spread: {mean*100:+.4f}%")
print(f"  long leg (top-3) mean: {lmean*100:+.4f}%   short leg (bot-3): {smean*100:+.4f}%")
print(f"Std dev (monthly)      : {sd*100:.4f}%")
print(f"t-statistic            : {tstat:+.3f}")
print(f"Annualised (mean x12)  : {ann:+.2f}%")
print(f"Sharpe (ann, spot)     : {sharpe:+.3f}")
print(f"Win rate (months >0)   : {winrate:.1f}%")
print(f"Profit factor          : {pf:.3f}")
print(f"Max drawdown (equity)  : {mdd*100:.2f}%")
print("-"*64)
sig_ok = tstat>2.0
sign_ok = mean>0
print("PASS criteria: mean>0  AND  correct sign (winners>losers)  AND  t>2")
print(f"  mean>0          : {'YES' if sign_ok else 'NO'}")
print(f"  correct sign    : {'YES' if sign_ok else 'NO'}  (long-short positive => winners beat losers)")
print(f"  t>2 significant : {'YES' if sig_ok else 'NO'}  (t={tstat:+.3f})")
verdict = "PASS -> proceed to Gate 3 (OOS)" if (sign_ok and sig_ok) else "KILL"
print("="*64)
print(f"GATE 2 VERDICT: {verdict}")
print("="*64)
