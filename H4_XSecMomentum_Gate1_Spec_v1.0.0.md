# H4 — Cross-Sectional Currency Momentum — Gate 1 Rule-Set Specification

**Version:** v1.0.0
**Hypothesis:** H4 (Tier 2) — cross-sectional currency momentum (basket)
**Gate:** 1 — strict, discretion-free rule set (paper/pseudocode; no code)
**Status:** LOCKED. Pre-registered from theory. Alternatives are Gate 5 robustness checks, NOT a Gate 2 search.
**Companion:** Forex_Strategy_Validation_Playbook (gate pipeline), Forex_Hypothesis_Library (H4 entry).

---

## 0. GATE 0 CARRY-FORWARD (one-line)

Named inefficiency: relative-strength persistence across currencies driven by gradual
information diffusion + a risk premium loading on global crash risk. Pre-registered
direction: LONG strongest trailing, SHORT weakest trailing. Counterparty is partly
speculative (value/contrarian) — logged as the soft point. Gate 0 verdict: PASS.

---

## 1. UNIVERSE (settled)

Nine currencies ranked vs USD; USD is the numeraire and is NOT ranked.

EUR, GBP, AUD, CHF, JPY, NZD, CAD, SEK, NOK

Data: fx_data/<PAIR>_daily.csv, daily bid+ask, UTC/midnight-aligned, Mon-Fri,
frozen 2005-01-02 .. 2026-06-11. Source pairs: EURUSD, GBPUSD, AUDUSD, USDCHF,
USDJPY, NZDUSD, USDCAD, USDSEK, USDNOK.

---

## 2. RETURN NORMALISATION (mechanics, not a parameter)

Every series must read as "USD value of one unit of the foreign currency" before ranking,
so that a rising series ALWAYS means the foreign currency strengthening vs USD.

- Foreign-base pairs (EURUSD, GBPUSD, AUDUSD, NZDUSD): already foreign-per-USD priced
  as USD-per-foreign close; use close directly.
- USD-base pairs (USDCHF, USDJPY, USDCAD, USDSEK, USDNOK): INVERT (1/price) so the
  resulting series rises when the foreign currency strengthens.

Ranking uses spot mid close (c_mid). Bid/ask reserved for Gate 4 costs.

---

## 3. SIGNAL & RANKING

- Formation lookback L = 3 calendar months (~63 trading days). Pre-registered.
  Rationale: FX momentum is shorter-lived than equity momentum; 1-3m formation is the
  documented strong window (Menkhoff-Sarno-Schmeling-Schrimpf 2012). 3m balances signal
  strength against turnover for a hands-off monthly book.
- NO skip month. FX does not show the equity 1-month reversal, so no 12-1 style gap.
- Signal = trailing return over L of each normalised series, measured to the
  rebalance date close.
- Rank all 9 by trailing return, descending.

---

## 4. PORTFOLIO CONSTRUCTION

- Legs k = 3 (terciles). 9 names -> top-3 LONG, bottom-3 SHORT, middle-3 FLAT.
- Equal weight within each leg. Gross long = gross short (dollar-neutral by construction;
  the shared-USD leg cancels — pure relative strength, no residual dollar bet).
- 6 active positions per period.

---

## 5. REBALANCE & HOLDING

- Rebalance monthly, on the last trading day of each calendar month.
- Holding period = 1 month, tied to rebalance (not an independent parameter).
- Rank on last-trading-day close; hold through the next month; measure close-to-close.

---

## 6. SIZING

Flat / equal-weight within leg during validation. No volatility targeting, no scaling.
Non-negotiable for Gates 2-5.

---

## 7. RETURN CONVENTION & CARRY

- Gates 2-3: SPOT returns only (price change of normalised series). Keeps the momentum
  signal pure and tests H4's "uncorrelated to carry" thesis honestly.
- Swap/carry is introduced at Gate 4 as a real cost/return component — does carry help
  or hurt the spot-momentum book? It is NOT part of the signal or the Gate 2-3 return.

---

## 8. FREE-PARAMETER COUNT

Three: (1) lookback L = 3m, (2) legs k = 3, (3) rebalance = monthly.
Under the <5 ceiling. Everything else is mechanics or pre-registered convention.

---

## 9. IN-SAMPLE / OUT-OF-SAMPLE SPLIT (SEALED)

- In-sample (build): 2005-01-02 .. 2017-12-31  (~13.0 yrs, ~60.6%, ~156 monthly periods)
- Out-of-sample (SEALED): 2018-01-01 .. 2026-06-11  (~39.4%)

OOS is sealed until Gate 3. No peeking, no tuning to it. Optimising on OOS destroys the test.

---

## 10. PASS / FALSIFICATION (Gate 2)

PASS (Gate 2, in-sample):
- Mean monthly long-short spread > 0.
- Sign matches the pre-registered direction (winners > losers).
- Meaningful significance (target 100+ obs; we have ~156). Report mean, t-stat,
  win rate, profit factor, max drawdown, expectancy.

FALSIFICATION (kill the hypothesis):
- Long-short spread is the wrong sign, OR
- Statistically insignificant in-sample, OR (later)
- Sign flips / collapses OOS at Gate 3, OR
- Does not survive realistic costs at Gate 4.

H1, H2, H3 all died on exactly these conditions. H4 gets no softer a bar.

---

## 11. WHAT GATE 1 DOES NOT DECIDE (deferred, pre-logged)

Gate 5 robustness (NOT a Gate 2 search): L in {1, 6, 12} months; k = top/bottom-2;
weekly rebalance; vol-weighting. Gate 4: direct-cross execution to halve per-leg cost;
swap/carry component. None of these touch the locked primary spec above.

---

*Gate 1 verdict: LOCKED. Proceed to Gate 2 (in-sample backtest) in a fresh session.*
