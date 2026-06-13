#!/usr/bin/env python3
# H5 Carry - Gate 2 Stage 2: IN-SAMPLE backtest (2005-01-02..2017-12-31). Pure stdlib. Read-only.
# Cross-sectional carry: rank 9 ccy vs USD by BIS policy rate, top-3 long / bottom-3 short,
# equal-weight (+/-1/3), dollar-neutral, monthly rebalance (1st trading day), daily spot(mid)+carry
# (act/360, weekend handled by calendar-day gap). OOS (2018+) NEVER touched here.
import csv, glob, os, sys, math, bisect
from datetime import date
from collections import defaultdict, OrderedDict

IS_START = date(2005, 1, 2)
IS_END   = date(2017, 12, 31)

CCY2CODE = OrderedDict([('USD','US'),('EUR','XM'),('GBP','GB'),('AUD','AU'),('CHF','CH'),
                        ('JPY','JP'),('NZD','NZ'),('CAD','CA'),('SEK','SE'),('NOK','NO')])
PAIRS = OrderedDict([('EUR',('EURUSD','CCYUSD')),('GBP',('GBPUSD','CCYUSD')),
                     ('AUD',('AUDUSD','CCYUSD')),('NZD',('NZDUSD','CCYUSD')),
                     ('CHF',('USDCHF','USDCCY')),('JPY',('USDJPY','USDCCY')),
                     ('CAD',('USDCAD','USDCCY')),('SEK',('USDSEK','USDCCY')),
                     ('NOK',('USDNOK','USDCCY'))])
TRADE_CCY = list(PAIRS.keys())

def parse_date(s):
    s = s.strip()[:10]
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))

# ---- load BIS policy rates (daily only; split 'CODE: Label' on ':') ----
csvs = sorted(glob.glob('cbpol_raw/**/*.csv', recursive=True), key=lambda p: -os.path.getsize(p))
if not csvs: print('NO CBPOL CSV'); sys.exit(1)
cpath = csvs[0]
with open(cpath, encoding='utf-8-sig') as f: first = f.readline()
delim = ';' if first.count(';') > first.count(',') else ','
with open(cpath, newline='', encoding='utf-8-sig') as f:
    header = next(csv.reader(f, delimiter=delim))
def find(names):
    for i, c in enumerate(header):
        cu = c.upper()
        for n in names:
            if n in cu: return i
    return -1
iF, iA, iT, iV = find(['FREQ']), find(['REF_AREA']), find(['TIME_PERIOD','TIME']), find(['OBS_VALUE','VALUE'])
if min(iF, iA, iT, iV) < 0: print('col detect fail', header); sys.exit(1)
code2ccy = {v: k for k, v in CCY2CODE.items()}
rates = defaultdict(list)
with open(cpath, newline='', encoding='utf-8-sig') as f:
    r = csv.reader(f, delimiter=delim); next(r)
    for row in r:
        if len(row) <= max(iF, iA, iT, iV): continue
        fr = row[iF].split(':')[0].strip()
        ar = row[iA].split(':')[0].strip()
        if fr != 'D' or ar not in code2ccy: continue
        v = row[iV].strip()
        if v == '': continue
        try: val = float(v)
        except ValueError: continue
        if math.isnan(val): continue
        rates[code2ccy[ar]].append((parse_date(row[iT]), val))
for c in rates: rates[c].sort()
rate_dates = {c: [d for d, _ in rates[c]] for c in rates}
rate_vals  = {c: [v for _, v in rates[c]] for c in rates}
def rate_on(c, d):
    ds = rate_dates.get(c)
    if not ds: return None
    i = bisect.bisect_right(ds, d) - 1
    return rate_vals[c][i] if i >= 0 else None

# ---- load FX mids ----
def load_pair(base):
    path = None
    for cand in ['fx_data/%s.csv' % base] + glob.glob('fx_data/*%s*.csv' % base):
        if os.path.exists(cand): path = cand; break
    if not path: return None
    out = {}
    with open(path, newline='', encoding='utf-8-sig') as f:
        rd = csv.DictReader(f)
        cols = {k.lower(): k for k in rd.fieldnames}
        dk, mk = cols.get('date'), cols.get('c_mid')
        for row in rd:
            try:
                d = parse_date(row[dk]); m = float(row[mk])
            except (ValueError, TypeError, KeyError): continue
            if m > 0: out[d] = m
    return out
mids = {}
for ccy, (base, conv) in PAIRS.items():
    p = load_pair(base)
    if not p: print('MISSING FX FILE for', base); sys.exit(1)
    mids[ccy] = p

# trading calendar = dates where all 9 priced, within IS
alld = None
for ccy in TRADE_CCY:
    s = set(mids[ccy].keys())
    alld = s if alld is None else (alld & s)
cal = sorted(d for d in alld if IS_START <= d <= IS_END)

# ---- integrity ----
print('==== INTEGRITY ====')
print('CBPOL file:', cpath)
print('Trading days (all-9-priced, IS):', len(cal), ' span', cal[0], '->', cal[-1])
chk = cal[0]  # first actual trading day = first ranking date
ok = True
for c in CCY2CODE:
    ds = rate_dates.get(c)
    has = rate_on(c, chk) is not None
    print('  %-3s rate n=%-6s first=%-12s on_%s=%s  val=%s'
          % (c, len(ds) if ds else 0, ds[0] if ds else None, chk, has, rate_on(c, chk)))
    if not has: ok = False
print('All 10 have a rate by first trading day (%s):' % chk, ok)
if not ok: print('*** ABORT: rate gap at first trading day ***'); sys.exit(1)

# ---- backtest ----
def first_trading_days(cal):
    out = set(); prev = None
    for d in cal:
        ym = (d.year, d.month)
        if ym != prev: out.add(d); prev = ym
    return out
rebal_days = first_trading_days(cal)

def long_ccy_spot_ret(ccy, d_prev, d):
    base, conv = PAIRS[ccy]
    p0, p1 = mids[ccy][d_prev], mids[ccy][d]
    return (p1 / p0 - 1.0) if conv == 'CCYUSD' else (p0 / p1 - 1.0)

weights = {c: 0.0 for c in TRADE_CCY}
daily = []; nreb = 0; last_long = last_short = []
for i, d in enumerate(cal):
    if i > 0:  # return over [prev, d] using CURRENT (pre-existing) book - no look-ahead
        dprev = cal[i-1]; gap = (d - dprev).days
        ru = rate_on('USD', dprev); pr = 0.0
        for c in TRADE_CCY:
            w = weights[c]
            if w == 0.0: continue
            sret = long_ccy_spot_ret(c, dprev, d)
            carry = (rate_on(c, dprev) - ru) / 100.0 * (gap / 360.0)
            pr += w * (sret + carry)
        daily.append((d, pr))
    if d in rebal_days:  # update book at END of day d -> effective next period
        rk = sorted(TRADE_CCY, key=lambda c: rate_on(c, d), reverse=True)
        longs, shorts = rk[:3], rk[-3:]
        weights = {c: 0.0 for c in TRADE_CCY}
        for c in longs: weights[c] = 1.0/3
        for c in shorts: weights[c] = -1.0/3
        nreb += 1; last_long, last_short = longs, shorts

# monthly compound
monthly = OrderedDict()
for d, pr in daily:
    ym = (d.year, d.month)
    monthly.setdefault(ym, 1.0)
    monthly[ym] *= (1 + pr)
mret = [v - 1.0 for v in monthly.values()]
n = len(mret); mean = sum(mret)/n
std = math.sqrt(sum((x-mean)**2 for x in mret)/(n-1))
t = mean/(std/math.sqrt(n)) if std > 0 else float('nan')
pos = sum(x for x in mret if x > 0); neg = sum(x for x in mret if x < 0)
pf = pos/abs(neg) if neg != 0 else float('inf')
win = sum(1 for x in mret if x > 0)/n
eq = peak = 1.0; mdd = 0.0
for x in mret:
    eq *= (1+x); peak = max(peak, eq); mdd = min(mdd, eq/peak - 1)
sharpe = mean/std*math.sqrt(12) if std > 0 else float('nan')

print('\n==== GATE 2 IN-SAMPLE RESULT (2005-2017) ====')
print('Rebalances: %d   Trading days: %d   Months: %d' % (nreb, len(cal), n))
print('Last rebalance LONG :', last_long)
print('Last rebalance SHORT:', last_short)
print('Mean monthly L-S : %+.4f%%' % (mean*100))
print('Std  monthly     :  %.4f%%' % (std*100))
print('t-stat           : %+.3f' % t)
print('Annualised mean  : %+.2f%%' % (mean*12*100))
print('Ann. Sharpe      : %+.2f' % sharpe)
print('Profit factor    :  %.2f' % pf)
print('Win-rate (months):  %.1f%%' % (win*100))
print('Max drawdown     :  %.2f%%' % (mdd*100))
print('SIGN             :', 'POSITIVE - long-high > short-low - PRE-REGISTERED DIRECTION CONFIRMED'
      if mean > 0 else 'NEGATIVE/ZERO - WRONG SIGN')
