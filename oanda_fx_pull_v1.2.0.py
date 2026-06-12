#!/usr/bin/env python3
"""
oanda_fx_pull_v1.2.0.py — daily FX puller. G10-vs-USD basket for H4
cross-sectional momentum (adds NZD,CAD,SEK,NOK to the original 5).
Sibling to oanda_index_pull_v1.0.0.py. Indices give the SIGNAL; these pairs
give the traded RETURN. Same CSV format, same fail-closed discipline.
--to end-caps the pull at the frozen range end so new pairs align
exactly with the existing 5. Output: fx_data/<PAIR>_daily.csv.
ENV: OANDA_TOKEN, OANDA_ACCOUNT, OANDA_ENV ('practice'|'live').
"""
import os, sys, csv, time, argparse
from datetime import datetime, timezone
try:
    import requests
except ImportError:
    sys.exit("ERROR: requests not installed. Run: pip install requests")

PAIRS = {
    "EUR_USD": "EURUSD", "GBP_USD": "GBPUSD", "AUD_USD": "AUDUSD",
    "USD_CHF": "USDCHF", "USD_JPY": "USDJPY",
    "NZD_USD": "NZDUSD", "USD_CAD": "USDCAD",
    "USD_SEK": "USDSEK", "USD_NOK": "USDNOK",
}
GRANULARITY="D"; PRICE="BA"; PAGE_COUNT=5000
DEFAULT_FROM="2005-01-01"; DEFAULT_TO="2026-06-11"
OUTPUT_DIR="fx_data"; REQUEST_PACING=0.15

def get_config():
    token=os.environ.get("OANDA_TOKEN"); account=os.environ.get("OANDA_ACCOUNT")
    env=os.environ.get("OANDA_ENV","practice").lower()
    if not token: sys.exit("ERROR: OANDA_TOKEN not set. Fail-closed, aborting.")
    if not account: sys.exit("ERROR: OANDA_ACCOUNT not set. Fail-closed, aborting.")
    host=("https://api-fxtrade.oanda.com" if env=="live"
          else "https://api-fxpractice.oanda.com")
    return token, account, host, env

def session_for(token):
    s=requests.Session()
    s.headers.update({"Authorization":f"Bearer {token}",
        "Content-Type":"application/json","Accept-Datetime-Format":"RFC3339"})
    return s

def rfc3339(d):
    dt=datetime.strptime(d,"%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00","Z")

def list_instruments(sess, account, host):
    r=sess.get(f"{host}/v3/accounts/{account}/instruments", timeout=30)
    if r.status_code!=200:
        sys.exit(f"ERROR: list instruments ({r.status_code}): {r.text[:300]}")
    return {i["name"] for i in r.json().get("instruments",[])}

def probe(sess, account, host):
    avail=list_instruments(sess, account, host)
    print("\n"+"="*60); print("PHASE 1 — PROBE"); print("="*60)
    print(f"{'INSTRUMENT':<12}{'OUTPUT':<10}EXISTS"); print("-"*60)
    resolved={}
    for inst, base in PAIRS.items():
        ok=inst in avail
        print(f"{inst:<12}{base:<10}{'yes' if ok else 'no  <-- MISSING'}")
        resolved[inst]=base if ok else None
    print("-"*60); return resolved

def fetch(sess, host, inst, params):
    params = {**params, "alignmentTimezone": "UTC", "dailyAlignment": 0}
    r=sess.get(f"{host}/v3/instruments/{inst}/candles", params=params, timeout=30)
    if r.status_code!=200: return None, f"{r.status_code}: {r.text[:200]}"
    return r.json().get("candles",[]), None

def first_candle(sess, host, inst, frm):
    c,e=fetch(sess,host,inst,{"granularity":GRANULARITY,"price":PRICE,
        "from":rfc3339(frm),"count":1,"includeFirst":True})
    return None if (e or not c) else c[0]["time"][:10]

def last_candle(sess, host, inst):
    c,e=fetch(sess,host,inst,{"granularity":GRANULARITY,"price":PRICE,"count":1})
    return None if (e or not c) else c[-1]["time"][:10]

def depth(sess, host, resolved, frm):
    print("\n"+"="*60); print("PHASE 2 — DEPTH"); print("="*60)
    print(f"{'INSTRUMENT':<12}{'FIRST':<12}LAST"); print("-"*60)
    for inst, base in resolved.items():
        if base is None: continue
        f=first_candle(sess,host,inst,frm); time.sleep(REQUEST_PACING)
        l=last_candle(sess,host,inst); time.sleep(REQUEST_PACING)
        print(f"{inst:<12}{str(f):<12}{str(l)}")
    print("-"*60)

def pull_one(sess, host, inst, frm, to):
    rows=[]; cursor=rfc3339(frm); seen=set(); capped=False
    while True:
        c,e=fetch(sess,host,inst,{"granularity":GRANULARITY,"price":PRICE,
            "from":cursor,"count":PAGE_COUNT,"includeFirst":True})
        if e: print(f"  WARN {inst}: {e}"); break
        if not c: break
        new=0
        for k in c:
            if not k.get("complete",False): continue
            t=k["time"][:10]
            if to and t>to: capped=True; break   # frozen end-cap, candles ascending
            if t in seen: continue
            seen.add(t); new+=1
            b,a=k["bid"],k["ask"]; mid=(float(b["c"])+float(a["c"]))/2
            rows.append([t,b["o"],b["h"],b["l"],b["c"],
                a["o"],a["h"],a["l"],a["c"],f"{mid:.5f}",k.get("volume",0)])
        if capped: break
        if len(c)<PAGE_COUNT: break
        cursor=c[-1]["time"]; time.sleep(REQUEST_PACING)
        if new==0: break
    return rows

def write_csv(base, rows):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    p=os.path.join(OUTPUT_DIR,f"{base}_daily.csv")
    with open(p,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["date","o_bid","h_bid","l_bid","c_bid",
            "o_ask","h_ask","l_ask","c_ask","c_mid","volume"])
        w.writerows(rows)
    return p

def pull(sess, host, resolved, frm, to):
    print("\n"+"="*60); print("PHASE 3 — PULL"); print("="*60)
    print(f"  end-cap (frozen): {to}")
    for inst, base in resolved.items():
        if base is None: continue
        print(f"  pulling {inst} ...", end=" ", flush=True)
        rows=pull_one(sess,host,inst,frm,to)
        if not rows: print("no data"); continue
        p=write_csv(base,rows)
        print(f"{len(rows)} rows -> {p} ({rows[0][0]} .. {rows[-1][0]})")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--pull",action="store_true")
    ap.add_argument("--from",dest="from_date",default=DEFAULT_FROM)
    ap.add_argument("--to",dest="to_date",default=DEFAULT_TO)
    args=ap.parse_args()
    token,account,host,env=get_config()
    sess=session_for(token)
    print(f"Oanda env: {env}  host: {host}")
    resolved=probe(sess,account,host)
    depth(sess,host,resolved,args.from_date)
    if args.pull: pull(sess,host,resolved,args.from_date,args.to_date)
    else: print("\nProbe + depth done. Re-run with --pull when the table looks right.")

if __name__=="__main__":
    main()
