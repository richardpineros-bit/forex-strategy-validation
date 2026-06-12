# H3 - Month-End FX Rebalancing Flow - Gate 2 Results

**Version:** v1.0.0
**Gate:** 2 - In-sample backtest (exit <= 2017-12-31). OOS (>=2018) SEALED, untouched.
**Spec:** H3_MonthEnd_Gate1_Spec_v1.0.0.md (locked)  |  **Backtest:** h3_gate2_backtest_v1.0.0.py
**Data:** UTC/midnight-aligned daily mids, frozen (commit ebc1390). Mon-Fri only.
**Verdict:** KILL

## Results - in-sample

| Pair | n | mean bps | t | win % | PF |
|------|----|---------|------|-------|------|
| EURUSD | 156 | -6.37 | -0.66 | 44.9 | 0.87 |
| GBPUSD | 155 | -4.32 | -0.39 | 49.0 | 0.91 |
| AUDUSD | 156 | +3.50 | 0.28 | 49.4 | 1.06 |
| USDCHF | 156 | +3.53 | 0.32 | 50.6 | 1.07 |
| CORE-4 pooled (raw) | 623 | -0.91 | -0.16 | 48.5 | 0.98 |
| CORE-4 pooled (winsorised 1/99) | 623 | -1.15 | -0.22 | 48.5 | 0.98 |

- Per-pair sign consistency: 2/4 positive - coin flip.
- Pooled t overstates significance (shared USD leg correlates the four); even so it is ~0.
- Avg hold 5.00 trading days; time-in-market ~23% of pair-days.
- SNB Jan-2015 USDCHF trade: entry 2015-01-23 -> exit 2015-01-30, -454.2 bps (shown, not dropped). Winsorising it changes nothing.
- USDJPY satellite: 0 in-sample trades (JP225Y starts 2020-04-27). Parked for Gate 3.

## Why KILL

1. Pre-registered direction is wrong-signed/absent pooled across the core (mean -0.91 bps, t -0.16) - the Gate 1 falsification condition, hit directly.
2. 2/4 sign consistency - no coherent cross-pair effect.
3. Not strongly inverted either (t -0.16) - the effect is absent at daily resolution, not reversed.
4. Mechanism: the rebalancing flow concentrates in the minutes around the benchmark fix; a daily-bar, 5-day-hold representation dilutes it to noise. Capturing it needs intraday data + intraday execution - incompatible with a no-screen-time, fully-automated constraint.

No direction flip. No parameter search. Killed on the build data, zero capital - same discipline as H1 (died OOS) and H2 (died in-sample). All three Tier-1 hypotheses now exhausted; next candidate is Tier 2 / H4.
