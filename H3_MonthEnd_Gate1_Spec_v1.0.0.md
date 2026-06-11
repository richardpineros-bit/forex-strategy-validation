# H3 — Month-End FX Rebalancing Flow (equity-conditional)
## GATE 1 — Strict Rule Set (locked)

**Version:** v1.0.0
**Pipeline:** Forex Strategy Validation Playbook v1.0.2
**Status:** Gate 0 PASS → Gate 1 locked. Next: Gate 2 in-sample backtest.
**Prior:** Moderate (Melvin & Prins 2015 is published; OOS straddles publication).

---

## 1. MECHANISM (one line)
US-based global equity funds hedge foreign-equity FX exposure; when foreign
equity outperforms US equity over the month, they must sell more of the
foreign currency into the month-end fix to restore the hedge ratio. That
forced, price-insensitive flow drives a forecastable month-end FX move.

---

## 2. UNIVERSE

**Core basket (pooled, full history 2005→2026):**
| Pair | Home index (local) | Benchmark | Foreign ccy is |
|------|--------------------|-----------|----------------|
| EURUSD | EU50_EUR | SPX500_USD | BASE |
| GBPUSD | UK100_GBP | SPX500_USD | BASE |
| AUDUSD | AU200_AUD | SPX500_USD | BASE |
| USDCHF | CH20_CHF | SPX500_USD | QUOTE |

**Satellite (reported separately, NEVER pooled with core):**
| USDJPY | JP225Y_JPY | SPX500_USD | QUOTE | from 2020-04-27 only |

Index returns are measured in each index's **local currency** (this is why
JP225Y_JPY, not JP225_USD — the USD-denominated Nikkei bakes in the very FX
move we are predicting; circular, banned).

---

## 3. THE SIGNAL (mechanical, look-ahead-free)

For each calendar month, for each pair:

- `month_start` = first trading day of the calendar month.
- `entry_day`   = the trading day **N = 5** positions before the last trading
  day of the month (LTD). (entry index = LTD index − 5.)
- Compute month-to-date log returns, using closes **through entry_day only**:
  - `r_home = ln(home_close[entry_day] / home_close[month_start])`
  - `r_spx  = ln(spx_close[entry_day]  / spx_close[month_start])`
- `s = sign(r_home − r_spx)`  → +1 home outperforms, −1 home underperforms.

No future data is used: the signal window ends at entry_day close, and the
trade we measure runs from entry_day close to exit. Clean.

---

## 4. DIRECTION (pre-registered, never data-picked)

`base_sign = +1` if foreign ccy is BASE (EUR/GBP/AUD-USD),
`base_sign = −1` if foreign ccy is QUOTE (USDCHF, USDJPY).

```
dir = −sign(s) × base_sign
```

Verification of the wiring:
- Home outperforms (s = +1) → sell foreign currency:
  - foreign BASE  → dir = −1 (SHORT pair)  ✓
  - foreign QUOTE → dir = +1 (LONG pair)   ✓
- Home underperforms (s = −1) → buy foreign currency:
  - foreign BASE  → dir = +1 (LONG pair)   ✓
  - foreign QUOTE → dir = −1 (SHORT pair)  ✓

If `s = 0` (effectively never on continuous data): no trade.

---

## 5. ENTRY / EXIT / HOLD

- **Entry:** at the close of `entry_day` (N=5 trading days before LTD).
- **Exit:**  at the close of the LTD (month-end fix approximation).
- **Hold:**  ~5 trading days. Time-based only.
- **Stop:**  NONE. **Target:** NONE. The hypothesis is directional drift over
  the rebalancing window; a stop/target would add free parameters and is not
  part of the mechanism. Stops are a Gate 5 refinement question, not Gate 1.

---

## 6. SIZING & RETURNS

- **Sizing:** flat / one unit per signal, equal weight across pairs. No scaling.
- **Price:** mid for Gates 2–3; bid/ask spread applied at Gate 4.
- **Signed return:**
  `ret_bps = dir × ln(exit_mid / entry_mid) × 10000`
  (signed so a correct directional call reads positive.)

---

## 7. FILTERS
**None.** No news filter (month-end flow *is* the signal; filtering it removes
the edge). No magnitude threshold on `s` (sign-only is pre-registered; a
threshold is a free parameter held for Gate 5). Clean and minimal by design.

---

## 8. FREE-PARAMETER COUNT
| Parameter | Primary value | Free? |
|-----------|---------------|-------|
| Entry offset N | 5 days before LTD | YES (1) |
| Exit offset | 0 (LTD close) | YES (1) |
| Signal lookback | month-to-date (fixed by mechanism) | no |
| Signal threshold | 0 / sign-only (fixed by theory) | no |
| Direction | mechanical from signal | no |
| Stop / target | none | no |

**Free parameters = 2. Under the 5 cap. PASS.**

Alternatives held for **Gate 5 robustness only** (NOT a Gate 2 search):
N ∈ {1, 3, 5, 7}; exit offset ∈ {−1, 0, +1}; magnitude threshold on s.

---

## 9. SPLIT (locked, sealed)
- Chronological, by exit date.
- **In-sample:** trades with exit date ≤ **2017-12-31** (~60%).
- **Out-of-sample (SEALED):** exit date ≥ **2018-01-01** (~40%).
- OOS is not opened, peeked at, or tuned against until Gate 3. Once optimised
  against, it is dead as a test.

---

## 10. REPORTING (per gate)
Trades, mean ret + t-stat (`t = mean/(std/√n)`), win rate, profit factor,
equity curve, max drawdown, time-in-market, worst single drawdown.
**Pool the core 4 BUT report per-pair sign consistency** — pooled t overstates
significance because the shared USD leg correlates the trades.

---

## 11. FALSIFICATION (kill conditions, fixed up front)
- In-sample: pre-registered direction absent or wrong-signed pooled across core.
- OOS: sign flips on the sealed 40%.
- Costs: per-event edge < spread (short holds → spread dominates at Gate 4).

---

## CARRIED RISKS (honest, not hidden)
1. **Daily-data dilution.** Melvin-Prins is an intraday, minutes-around-the-fix
   effect. Daily candles approximate it with a 5-day hold, diluting concentrated
   flow with overnight noise. This is the most likely reason a real effect
   washes out at Gate 2. Expected, not a Gate 1 kill.
2. **2015-01 SNB de-peg** sits in USDCHF in-sample — a violent outlier that will
   distort the t-stat if untreated. Handle at Gate 2 (winsorise/flag, do not
   silently drop).
3. **Publication crowding.** Effect is public since 2015; OOS (2018→) tests
   whether it decayed. Keep the prior moderate.

---

**Gate 1 verdict: PASS.** Zero discretion, 2 free parameters, split sealed,
falsification fixed. Proceed to Gate 2 in-sample backtest.
