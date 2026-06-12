# H4 — Cross-Sectional Currency Momentum — Gate 2 Results

**Version:** v1.0.0
**Hypothesis:** H4 (Tier 2) — cross-sectional currency momentum (basket)
**Gate:** 2 — in-sample backtest (2005-01-02 .. 2017-12-31). OOS 2018+ SEALED, not loaded.
**Spec:** H4_XSecMomentum_Gate1_Spec_v1.0.0 (run verbatim, no deviation).
**Backtest:** h4_gate2_backtest_v1.0.0.py (pure stdlib).
**Verdict:** KILL.

---

## RESULT (in-sample, n = 152 monthly L-S observations)

| Metric | Value |
|--------|-------|
| Mean monthly L-S spread | -0.0835% |
| Long leg (top-3) mean | +0.0185% / month |
| Short leg (bot-3) mean | +0.1020% / month |
| Monthly std | 2.2912% |
| t-statistic | -0.449 |
| Annualised (mean x12) | -1.00% |
| Sharpe (ann, spot) | -0.126 |
| Win rate (months > 0) | 45.4% |
| Profit factor | 0.909 |
| Max drawdown (equity) | -28.97% |

First held month 2005-05, last 2017-12. 156 aligned month-ends.

---

## PASS / FALSIFICATION CHECK

Pre-registered PASS: mean > 0 AND correct sign (winners > losers) AND t > 2.
- mean > 0 .......... NO (-0.0835%)
- correct sign ....... NO (losers outperformed winners; faint reversal tilt)
- t > 2 significant .... NO (t = -0.449)

Falsification condition met on the first and primary criterion: wrong sign AND
statistically insignificant in-sample. KILL.

---

## INTEGRITY (this is a real result, not a bug)

Verified before declaring KILL:
- Normalisation correct: USD-base pairs inverted (USDJPY ~0.009 = 1/110;
  USDSEK/NOK ~0.12 = 1/8). Foreign-base direct. No zeros, no explosions.
- Per-currency annualised returns all realistic single digits (-2.5% .. +1.6%).
- Sample rankings economically sane: Sep-2008 (GFC) ranks JPY strongest
  (safe-haven bid), AUD weakest (risk-off). The ranker reads the tape correctly.

Mechanics sound; the edge is genuinely absent at the pre-registered spec.

---

## INTERPRETATION (why the documented ~10% did not appear)

The headline currency-momentum premium in the literature is typically built on a
much broader basket (often 20-48 currencies including EM) and on returns that blend
SPOT with FORWARD POINTS / CARRY. This spec deliberately isolated PURE SPOT on a
developed G10 basket, to honour H4's "uncorrelated to carry" claim and keep the
momentum signal clean. Pure-spot developed-FX momentum is far weaker in the
literature; here it is absent (and faintly negative).

This is consistent with the better reading of the evidence, not a contradiction of it.

---

## DISCIPLINE NOTE (no rescue)

NOT done, deliberately:
- No search over L in {1,6,12} to find a winning lookback. That is curve-fitting a
  dead hypothesis. The pre-registered L=3 failed; that is the test.
- No bolting carry onto the signal to rescue the return. A carry-blended momentum
  is a DIFFERENT hypothesis requiring its own Gate 0 — not a modification of H4.

H4 is KILLED in-sample. It does not advance to Gate 3.

---

## STATUS

H4: KILLED (Gate 2, in-sample, t -0.449, wrong sign).
Tally: H1 killed (OOS), H2 killed (IS), H3 killed (IS), H4 killed (IS).
All Tier-1 and the first Tier-2 idea exhausted. Next candidate: H5 (carry) or H6
(London breakout) per the hypothesis library — fresh Gate 0 required.

*Gate 2 verdict: KILL. OOS never loaded. Audit trail preserved.*
