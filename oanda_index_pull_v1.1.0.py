#!/usr/bin/env python3
"""
oanda_index_pull_v1.1.0.py
==========================
Pull daily index-CFD candles from Oanda v20 for the H3 (equity-conditional
month-end flow) signal source.

Runs in three phases, in order:
  PHASE 1  PROBE   - which candidate instrument strings actually exist on
                     your account. Prints an availability table.
  PHASE 2  DEPTH   - for the ones that exist, fetch earliest + latest candle
                     dates so you know real history depth per index.
  PHASE 3  PULL    - paginated daily bid+ask pull, one CSV per instrument.

PHASE 3 only runs for instruments that pass PHASE 1, and only if you pass
--pull on the command line. Default run is probe + depth only (cheap, fast),
so you can report depth back before committing to the bulk pull.

ENV (do NOT hard-code secrets):
  OANDA_TOKEN     your v20 API token
  OANDA_ACCOUNT   your v20 account id (e.g. 001-011-1234567-001)
  OANDA_ENV       'practice' (default) or 'live'

USAGE:
  python3 oanda_index_pull_v1.1.0.py            # probe + depth only
  python3 oanda_index_pull_v1.1.0.py --pull     # also do the full CSV pull
  python3 oanda_index_pull_v1.1.0.py --pull --from 2005-01-01

Australian/UK spelling throughout. Fail-closed: missing token/account aborts.
"""

import os
import sys
import csv
import time
import argparse
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    sys.exit("ERROR: requests not installed. Run: pip install requests")

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------

# Candidate instrument strings to probe, grouped by the currency whose
# home-equity signal they provide. We PROBE rather than assume — the probe
# table is the source of truth on what your account actually offers.
#
# Each currency lists candidate strings in preference order. The first one
# that exists is treated as that currency's home index.
CANDIDATES = {
    "USD": ["SPX500_USD"],                      # S&P 500
    "EUR": ["EU50_EUR", "ESTX50_EUR"],          # EuroStoxx 50
    "JPY": ["JP225Y_JPY", "JP225_JPY", "JP225_USD"],  # Nikkei 225 (want JPY-denom)
    "GBP": ["UK100_GBP"],                        # FTSE 100
    "AUD": ["AU200_AUD"],                        # ASX 200
    # --- uncertain / likely-missing — probe honestly, expect gaps ---
    "CHF": ["CH20_CHF"],                         # Swiss 20 (SMI proxy)
    "CAD": ["CA60_CAD"],                         # TSX 60 (likely absent)
    "NZD": ["NZ50_NZD"],                         # NZX 50 (likely absent)
}

GRANULARITY = "D"
PRICE = "BA"          # bid + ask in each candle
PAGE_COUNT = 5000     # Oanda hard cap per request
DEFAULT_FROM = "2005-01-01"
OUTPUT_DIR = "index_data"
REQUEST_PACING = 0.15  # seconds between requests, be polite to the API

# --------------------------------------------------------------------------
# API PLUMBING
# --------------------------------------------------------------------------

def get_config():
    token = os.environ.get("OANDA_TOKEN")
    account = os.environ.get("OANDA_ACCOUNT")
    env = os.environ.get("OANDA_ENV", "practice").lower()

    if not token:
        sys.exit("ERROR: OANDA_TOKEN not set. Fail-closed, aborting.")
    if not account:
        sys.exit("ERROR: OANDA_ACCOUNT not set. Fail-closed, aborting.")

    host = ("https://api-fxtrade.oanda.com" if env == "live"
            else "https://api-fxpractice.oanda.com")
    return token, account, host, env


def session_for(token):
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept-Datetime-Format": "RFC3339",
    })
    return s


def rfc3339(date_str):
    """'2005-01-01' -> RFC3339 at UTC midnight."""
    dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


# --------------------------------------------------------------------------
# PHASE 1 — PROBE
# --------------------------------------------------------------------------

def list_account_instruments(sess, account, host):
    """Return the set of tradeable instrument names on the account."""
    url = f"{host}/v3/accounts/{account}/instruments"
    r = sess.get(url, timeout=30)
    if r.status_code != 200:
        sys.exit(f"ERROR: could not list instruments ({r.status_code}): {r.text[:300]}")
    data = r.json().get("instruments", [])
    return {i["name"] for i in data}


def probe(sess, account, host):
    available = list_account_instruments(sess, account, host)
    resolved = {}   # ccy -> chosen instrument (or None)

    print("\n" + "=" * 64)
    print("PHASE 1 — PROBE (which candidate strings exist on this account)")
    print("=" * 64)
    print(f"{'CCY':<5} {'CANDIDATE':<14} {'EXISTS':<8} {'CHOSEN'}")
    print("-" * 64)

    for ccy, cands in CANDIDATES.items():
        chosen = None
        for c in cands:
            exists = c in available
            mark = "yes" if exists else "no"
            star = ""
            if exists and chosen is None:
                chosen = c
                star = "  <-- using"
            print(f"{ccy:<5} {c:<14} {mark:<8}{star}")
        resolved[ccy] = chosen
        if chosen is None:
            print(f"{ccy:<5} {'(none)':<14} {'--':<8}  DROPPED from basket")
        print("-" * 64)

    return resolved


# --------------------------------------------------------------------------
# PHASE 2 — DEPTH
# --------------------------------------------------------------------------

def fetch_candles(sess, host, instrument, params):
    params = {**params, "alignmentTimezone": "UTC", "dailyAlignment": 0}
    url = f"{host}/v3/instruments/{instrument}/candles"
    r = sess.get(url, params=params, timeout=30)
    if r.status_code != 200:
        return None, f"{r.status_code}: {r.text[:200]}"
    return r.json().get("candles", []), None


def earliest_candle(sess, host, instrument, from_date):
    candles, err = fetch_candles(sess, host, instrument, {
        "granularity": GRANULARITY, "price": PRICE,
        "from": rfc3339(from_date), "count": 1, "includeFirst": True,
    })
    if err or not candles:
        return None
    return candles[0]["time"][:10]


def latest_candle(sess, host, instrument):
    candles, err = fetch_candles(sess, host, instrument, {
        "granularity": GRANULARITY, "price": PRICE, "count": 1,
    })
    if err or not candles:
        return None
    return candles[-1]["time"][:10]


def depth(sess, host, resolved, from_date):
    print("\n" + "=" * 64)
    print("PHASE 2 — DEPTH (real history per index)")
    print("=" * 64)
    print(f"{'CCY':<5} {'INSTRUMENT':<14} {'FIRST':<12} {'LAST':<12}")
    print("-" * 64)

    depths = {}
    for ccy, inst in resolved.items():
        if inst is None:
            continue
        first = earliest_candle(sess, host, inst, from_date)
        time.sleep(REQUEST_PACING)
        last = latest_candle(sess, host, inst)
        time.sleep(REQUEST_PACING)
        depths[ccy] = (inst, first, last)
        print(f"{ccy:<5} {inst:<14} {str(first):<12} {str(last):<12}")
    print("-" * 64)

    firsts = [d[1] for d in depths.values() if d[1]]
    if firsts:
        common = max(firsts)
        print(f"\nShortest common start (trim FX window to this): {common}")
        print("Basket with a usable home index:",
              ", ".join(c for c, d in depths.items() if d[1]))
    return depths


# --------------------------------------------------------------------------
# PHASE 3 — PULL
# --------------------------------------------------------------------------

def pull_instrument(sess, host, instrument, from_date):
    """Paginate forward, daily bid+ask, return list of rows."""
    rows = []
    cursor = rfc3339(from_date)
    seen = set()

    while True:
        candles, err = fetch_candles(sess, host, instrument, {
            "granularity": GRANULARITY, "price": PRICE,
            "from": cursor, "count": PAGE_COUNT, "includeFirst": True,
        })
        if err:
            print(f"  WARN {instrument}: {err}")
            break
        if not candles:
            break

        new = 0
        for c in candles:
            if not c.get("complete", False):
                continue
            t = c["time"][:10]
            if t in seen:
                continue
            seen.add(t)
            new += 1
            bid, ask = c["bid"], c["ask"]
            c_mid = (float(bid["c"]) + float(ask["c"])) / 2
            rows.append([
                t,
                bid["o"], bid["h"], bid["l"], bid["c"],
                ask["o"], ask["h"], ask["l"], ask["c"],
                f"{c_mid:.5f}", c.get("volume", 0),
            ])

        if len(candles) < PAGE_COUNT:
            break  # reached the end

        cursor = candles[-1]["time"]  # next page starts at last seen time
        time.sleep(REQUEST_PACING)
        if new == 0:
            break  # safety: no progress

    return rows


def write_csv(instrument, rows):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{instrument}_daily.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "date",
            "o_bid", "h_bid", "l_bid", "c_bid",
            "o_ask", "h_ask", "l_ask", "c_ask",
            "c_mid", "volume",
        ])
        w.writerows(rows)
    return path


def pull(sess, host, resolved, from_date):
    print("\n" + "=" * 64)
    print("PHASE 3 — PULL (daily bid+ask CSVs)")
    print("=" * 64)
    for ccy, inst in resolved.items():
        if inst is None:
            continue
        print(f"  pulling {ccy} {inst} ...", end=" ", flush=True)
        rows = pull_instrument(sess, host, inst, from_date)
        if not rows:
            print("no data")
            continue
        path = write_csv(inst, rows)
        print(f"{len(rows)} rows -> {path} ({rows[0][0]} .. {rows[-1][0]})")


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pull", action="store_true",
                    help="run the full CSV pull (default: probe + depth only)")
    ap.add_argument("--from", dest="from_date", default=DEFAULT_FROM,
                    help="start date YYYY-MM-DD (default 2005-01-01)")
    args = ap.parse_args()

    token, account, host, env = get_config()
    sess = session_for(token)
    print(f"Oanda env: {env}  host: {host}")

    resolved = probe(sess, account, host)
    depth(sess, host, resolved, args.from_date)

    if args.pull:
        pull(sess, host, resolved, args.from_date)
    else:
        print("\nProbe + depth complete. Re-run with --pull once you've")
        print("checked the depth table and confirmed the basket.")


if __name__ == "__main__":
    main()
