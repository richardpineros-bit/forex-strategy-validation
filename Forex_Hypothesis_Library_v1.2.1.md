# Forex Hypothesis Library — Candidate Edges & Resolved Results

**Version:** v1.2.1
**Companion to:** Forex Strategy Validation Playbook v1.0.7
**Purpose:** A lean ledger of trading hypotheses. For *resolved* ideas: the result and why it worked or didn't — so a dead idea is never re-tested. For *untested* ideas: a full thesis ready to feed into the gate pipeline.

**Changelog**
- v1.2.1 — H7 (liquidity-sweep, re-scoped to daily failed-breakout reversal) KILLED at Gate 0; moved to RESOLVED. Tier-3 pipeline now H8–H10. Companion ref → Playbook v1.0.7.
- v1.2.0 — Drift repair. H4, H5, H6 had been marked Killed in the status register (at v1.1.2–v1.1.3) but were never moved out of the untested pipeline or written into RESOLVED — the register and the body contradicted each other. Migrated all three to compact RESOLVED form with lessons; removed from the candidate pipeline. Corrected stale companion reference (was Playbook v1.0.3) to v1.0.5. Tier-2 queue now exhausted; Tier-3 (H7–H10) is next.
- v1.1.1 - H3 (month-end flow) recorded KILLED at Gate 2; moved to RESOLVED. Tier-1 pipeline now empty.
- v1.1.0 — Restructured: resolved hypotheses now compact (thesis · gate · verdict · lesson); untested kept full. Added graduation rule. H1 & H2 recorded as killed.
- v1.0.1 — H2 status → Killed at Gate 2.
- v1.0.0 — Initial library.

---

## HOW TO USE

- **The library tracks everything tersely.** One entry per hypothesis.
- **Run them in tier order** (Tier 1 first) — ranked by structural soundness and fit for hands-off, no-screen-time automation.
- **Graduation rule:** a hypothesis that **PASSES Gate 3 (out-of-sample)** has proven a *forward* edge and earns its own file — `Strategy_<Name>_v1.0.0.md`. From then on, that file is the single home for all its rules, parameters, and live notes. The library entry just points to it. Before Gate 3, the library entry is enough — no separate file.
- **Resolved = compact.** Killed/funded entries collapse to four lines: thesis · gate reached · verdict · lesson. The *lesson* is the asset — it's what stops you repeating the mistake.
- **Untested = full.** Keep the complete thesis until an idea is actually run.

### Ratings legend (1–5, 5 = best)
Structure · Auto · Life-fit · Fragility (5 = robust).

---

## STATUS REGISTER

| # | Hypothesis | Tier | Gate | Status |
|---|-----------|------|------|--------|
| H1 | Session drift | 1 | Gate 3 | **Killed** |
| H2 | Trend momentum | 1 | Gate 2 | **Killed** |
| H3 | Month-end flow | 1 | Gate 2 | **Killed** |
| H4 | X-sec momentum | 2 | Gate 2 | **Killed** |
| H5 | Carry | 2 | Gate 2 | **Killed** |
| H6 | London breakout | 2 | Gate 0 | **Killed** |
| H7 | Liquidity-sweep | 3 | Gate 0 | **Killed** |
| H8 | Round-number | 3 | — | Idea |
| H9 | Vol-compression breakout | 3 | — | Idea |
| H10 | Regime mean-reversion | 3 | — | Idea |

Statuses: Idea / Queued / Active / Killed / Funded.

---

## RESOLVED

### H1 — Intraday session drift ("home-vs-away") — KILLED
- **Thesis:** Majors drift directionally by session on recurring non-speculative flow (corporate hedging, fix, rebalancing). Pre-registered: short EUR/USD in EU hours, long in US hours (Breedon & Ranaldo 2013).
- **Reached:** Gate 3 (OOS). Passed Gate 2 strongly — t 3.93, stable across halves, not outlier-driven.
- **Verdict:** KILL — OOS t collapsed 3.93 → 0.20, PF 1.01, drawdown exceeded total return. Zero capital risked.
- **Lesson:** In-sample strength certifies nothing. Published flow anomalies get arbitraged away; only the sealed OOS catches decay. OOS is the sole truth — never peek, never re-tune to it.

### H2 — Time-series trend momentum on majors — KILLED
- **Thesis:** A major trending over ~12 months keeps trending. Sign of trailing 252-day return; long/short per pair; 7-major basket pooled; monthly rebalance.
- **Reached:** Gate 2 (in-sample) — failed on the build data itself.
- **Verdict:** KILL — pooled t 0.27, win 50.2%, PF 1.10 pre-cost, +2.7% return vs −30% max DD. 4/7 pairs positive = noise, not a basket edge. No rescue attempted.
- **Lesson:** Down-weight the prior when the counterparty is soft and the FX-specific evidence is contested. The headline "~10% p.a." was *cross-sectional* momentum's result (H4) borrowed onto a *time-series* idea whose own evidence is thin. Flat was the honest outcome; spectacular would have been a fitting tell.

### H3 - Month-end FX rebalancing flow (equity-conditional) - KILLED
- **Thesis:** US-based global equity funds hedge foreign-equity FX exposure; when foreign equity outperforms US over the month they must sell more foreign currency into the month-end fix (Melvin-Prins). Pre-registered: dir = -sign(home_MTD - SPX_MTD) x base_sign; entry LTD-5, exit LTD; daily mids; core EUR/GBP/AUD-USD + USDCHF.
- **Reached:** Gate 2 (in-sample, exit <=2017-12-31) - failed on the build data.
- **Verdict:** KILL - pooled core-4 t -0.16, mean -0.91bps, win 48.5%, PF 0.98; only 2/4 pairs positive. Winsorising the 2015 SNB outlier did not move it. Wrong-signed/absent in the pre-registered direction. No rescue. USDJPY satellite had 0 in-sample trades (JP225Y starts 2020).
- **Lesson:** A real intraday flow effect - the fix is minutes long - dilutes to noise across a 5-day daily-bar hold. Not automatable for a no-screen-time trader without intraday data and intraday execution. Do NOT flip the sign to chase the two negative pairs; that is the curve-fit trap.

### H4 — Cross-sectional currency momentum (basket) — KILLED
- **Thesis:** Long the strongest currencies, short the weakest, monthly rebalance; momentum expressed relatively across an 8+ currency basket, uncorrelated to carry. Literature headline: ~10% p.a. winner-minus-loser spread (the figure H2 mistakenly borrowed).
- **Reached:** Gate 2 (in-sample) — failed on the build data itself.
- **Verdict:** KILL — n152, mean −0.0835%/mo, t −0.449, wrong sign (faint reversal tilt), Sharpe −0.13, max DD −29%. No rescue.
- **Lesson:** The documented ~10% spread never appeared in-sample — it ran faintly *negative*. A wrong-signed result at t −0.449 over n152 is a kill. Do NOT flip to a reversal basket to chase the negative sign; that is the curve-fit trap. A well-cited premium is not a personal edge until your own sealed test confirms it.

### H5 — Carry trade (interest-rate differential) — KILLED
- **Thesis:** Long high-yield, short low-yield; collect the rate differential. Compensation for crash risk — UIP holds in bad times, so you're paid to bear the tail in good times.
- **Reached:** Gate 2 (in-sample). OOS left sealed (not consumed).
- **Verdict:** KILL — mean +0.12%/mo, t 0.62 (insignificant), Sharpe 0.17, max DD −30%. Correct sign, but t under 1 over a large sample = no significant edge.
- **Lesson:** A positive sign with t < 1 over a large sample is a KILL, not a "maybe". A heavily documented premium that can't clear significance in-sample has nothing to forward-test, and a weak positive expectancy strapped to a −30% crash tail is uninvestable for a small account.

### H6 — London-open range breakout — KILLED
- **Thesis:** Trade the break of the Asian range as London volume floods in (~35–40% of daily turnover passes through London).
- **Reached:** Gate 0 (feasibility) — killed before any code.
- **Verdict:** KILL — no intraday data on box, and the weakest persistence story in the queue: the mechanism supports *volatility*, not *direction*, and the counterparty is a predator stop-hunt rather than price-insensitive forced flow. Not worth sourcing hourly data to test the shakiest Gate 0.
- **Lesson:** A volatility mechanism is not a directional edge. When the counterparty is a predator (stop-hunting), not forced operational flow, the persistence story is weak — don't spend money or data-sourcing effort on the shakiest idea in the queue.

### H7 — Liquidity-sweep reversal (re-scoped to daily failed-breakout) — KILLED
- **Thesis:** Price sweeps a prior daily swing high/low (runs resting stops + breakout buy-stops) then closes back *inside* the level on the same daily bar; fade the failed breakout — sweep of highs → short, sweep of lows → long. Re-scoped from the original *intraday* sweep (untestable — box holds only daily data) to its daily-bar cousin.
- **Reached:** Gate 0 (paper). No code.
- **Verdict:** KILL — fails the PASS bar: no price-insensitive/forced counterparty, and no documented limits-to-arbitrage at the daily-hold scale. Stacks two known diseases — H3 (the only documented mechanism, Osler 2003 stop-cascades, is *intraday* and dilutes to noise on a daily hold) and H6 (counterparty is speculative: trapped breakout buyers / stop-hunt predators, who adapt). It was mechanically definable on daily bars (reclaim = close back inside) and inside the parameter budget, so it would NOT have died at Gate 1 — the edge *story* fails, not the rule.
- **Lesson:** A clean, automatable rule is not an edge — Auto was never H7's problem; persistence was. Re-scoping a hypothesis to fit the data you have tests the wrong thing: the daily proxy is not the intraday mechanic, and saying so out loud is the discipline. The daily failed-breakout may survive later as a *filter/confluence input*, never as a standalone edge.

---

## CANDIDATE PIPELINE (untested — full thesis)

### TIER 3 — Plausible but hard to automate / weaker evidence

#### H8 — Round-number reaction
- **Claim:** Price stalls/reverses at psychological levels (1.2000, 100.00).
- **Why it persists / counterparty:** Retail + bank order clustering and option barriers at round figures.
- **Ratings:** Structure 3 · Auto 3 · Life-fit 3 · Fragility 3. Small and pair-dependent — better as a *filter* than standalone.
- **Status:** Idea — use as a filter.

#### H9 — Volatility-compression breakout
- **Claim:** Enter on range expansion after a low-ATR squeeze.
- **Why it persists / counterparty:** Volatility clusters; compression precedes expansion. But direction at the break isn't given — needs a directional filter.
- **Ratings:** Structure 3 · Auto 4 · Life-fit 4 · Fragility 2 (regime-dependent, overfit-prone).
- **Status:** Idea — overfit-prone.

#### H10 — Regime-filtered mean reversion
- **Claim:** Fade stretches from a moving average, but *only* in ranging conditions.
- **Why it persists / counterparty:** Short-term overreaction corrects. But evidence conflicts — FX is called both "efficient/mean-reverting" and "more trending than reverting." That disagreement is itself a warning.
- **Ratings:** Structure 2 · Auto 3 · Life-fit 3 · Fragility 2. Lives or dies on the regime filter.
- **Status:** Idea — filter-dependent.

---

## THE PERSISTENCE TEST (vet any NEW idea before it earns a slot)

Ask in order:
1. **Who is on the other side, and why?** Can't name the loser → no edge.
2. **Is that counterparty price-insensitive (forced) or speculative?** Forced = durable. Speculative = probably already arbitraged.
3. **Why hasn't it been competed away?** Valid: too small for big capital, too risky (crash tail), too slow, capacity-constrained. "Nobody knows" is almost never true.
4. **What would falsify it?** Can't say → not testable → doesn't belong here.

### Edge families, ranked by typical durability
- **Flow-based / structural (most durable):** session drift, month-end fixes, index rebalancing, corporate hedging.
- **Risk-premium:** carry, value, momentum. Paid for bearing real risk — durable, with crash tails.
- **Behavioural:** under/over-reaction, anchoring, round numbers. Real but small and decay-prone; best as filters.
- **Microstructure:** liquidity sweeps, breakouts, session volatility. Real mechanics but crowded and discretion-heavy.
- **Regime-conditional:** mean reversion in ranges, breakout in compression. Lives or dies on the regime filter.

### Where to mine for new hypotheses
- Academic: SSRN, JFE, JMCB, BIS papers (flow/microstructure).
- Quant libraries: Quantpedia, RobotWealth, QuantRocket.
- Structural data: BIS Triennial Survey, broker/COT positioning.
- **Your own journal:** where do *you* already have positive expectancy? The cheapest edge to validate is one you already have.

### Blank Gate 0 template (copy for each new idea)
```
HYPOTHESIS #__ : <name>
(a) One-paragraph hypothesis:
(b) Named inefficiency & why it persists:
(c) Who is on the other side, and why they don't care:
(d) Rule skeleton (incl. pre-registered direction if research gives one):
(e) Falsification condition:
Gate 0 verdict: PASS / KILL
```

---

*Versioning: PATCH small edits, MINOR added/removed hypotheses or format change, MAJOR re-tiering/structural rewrite. Keep the status register in sync with the playbook's Part F. On Gate 3 PASS, spin out Strategy_<Name>_vX.Y.Z.md and point the entry to it.*
