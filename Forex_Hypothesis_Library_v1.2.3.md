# Forex Hypothesis Library — Candidate Edges & Resolved Results

**Version:** v1.2.3
**Companion to:** Forex Strategy Validation Playbook v1.0.9
**Purpose:** A lean ledger of trading hypotheses. For *resolved* ideas: the result and why it worked or didn't — so a dead idea is never re-tested. For *untested* ideas: a full thesis ready to feed into the gate pipeline.

**Changelog**
- v1.2.3 — H9 (volatility-compression breakout) KILLED at Gate 0, standalone; moved to RESOLVED. Tier-3 pipeline now H10 only. Not a feasibility death (squeeze-then-expand is observable on daily ATR — the H3/H8 granularity excuse does not apply); killed on the edge story. No directional prior survives theory: volatility clustering is magnitude not sign; HTF-trend continuation imports the dead H2 signal; gamma reasoning is magnitude; data-picks-the-side = curve-fit. Speculative/adaptive counterparty (H6 disease) + no daily limits-to-arb. A magnitude edge is not a direction edge; retain as volatility-timing filter, never standalone. Companion ref → Playbook v1.0.9.
- v1.2.2 — H8 (round-number reaction) KILLED at Gate 0; moved to RESOLVED. Tier-3 pipeline now H9–H10. Feasibility settled the verdict: on daily OHLC the only round-level proxy with testable frequency (approach-and-reject) fires at arbitrary non-round levels at the same rate (~24% round vs ~21% arbitrary, inside noise) — it measures generic bar shape, not a round-number reaction; the stricter pierce-and-reclaim definition fires on ~0.1% of bars (untestable). Companion ref → Playbook v1.0.8.
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
| H8 | Round-number | 3 | Gate 0 | **Killed** |
| H9 | Vol-compression breakout | 3 | Gate 0 | **Killed** |
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

### H8 — Round-number reaction — KILLED
- **Thesis:** Price stalls/reverses at psychological round levels (.00 big-figures, secondarily .50) via order clustering — take-profits bunch at the level (reversal), stops bunch just beyond (acceleration once breached) — plus bank defence of option barriers at round strikes (Osler 2003). Pre-registered direction = fade the approach (rally into level → short, fall into level → long); level set pre-registered (.00 primary, .50 secondary).
- **Reached:** Gate 0 (paper). No code.
- **Verdict:** KILL as a standalone. Feasibility decided it on the box's daily data: the strict proxy closest to Osler's mechanism (pierce a .00 then close back through, same bar) fires on ~0.1% of bars — ~7 events/pair in 20 years, untestable. The loose proxy (approach within ~15 pips, close rejects ~20 pips away) has frequency (~24% of bars) but a control test showed it rejects at arbitrary non-round levels (.37, .13) at the same ~21% rate — it measures generic daily bar shape (closes sit off the extremes), not a round-number reaction. The one durable strand — bank option-barrier defence (semi-forced counterparty, genuinely better than H6/H7's speculative one) — is real but unlocatable without intraday data and an options book.
- **Lesson:** Twin diseases again, now shown numerically. H3 disease: an intraday microstructure effect dilutes to nothing a daily bar can isolate from noise. And a forced counterparty you cannot *locate* with your data is not a tradeable edge — durability of the flow is necessary, observability is also necessary. The library's own pre-judgement held: real phenomenon, filter-grade only. Retain as confluence/context (don't buy straight into an overhead .00; flag round levels as S/R), never as a standalone system.

---

#### H9 — Volatility-compression breakout — KILLED
- **Thesis:** A low-ATR squeeze (volatility compression) precedes range expansion — ARCH/GARCH volatility clustering — so trade the break of the squeeze range. The coming move's MAGNITUDE is forecastable; its DIRECTION is not. Pre-registered direction attempted and failed: HTF-trend continuation imports the H2 trend-momentum signal already killed at Gate 2; dealer-gamma is a magnitude story (long gamma suppresses the range, short gamma amplifies the break) not a sign; ARCH clustering is variance, not drift. Letting the data choose the winning side = multiple-testing curve-fit, forbidden.
- **Reached:** Gate 0 (paper). No code.
- **Verdict:** KILL as a standalone. Explicitly NOT a feasibility death — squeeze-then-expand IS observable on daily ATR (ATR(n) low vs its own history, then a bar breaking the squeeze range), so the H3/H8 granularity excuse does not apply. Killed on the edge story: (1) no theory-given direction — the defining weakness, already conceded in the candidate line; (2) speculative/adaptive counterparty — whoever fades the range or provides liquidity during compression (range traders, mean-reversion algos, long-gamma dealers) gets run over on expansion but adapts; the H6 disease, crowded microstructure with the Judas-swing false-break problem; (3) no daily-scale limits-to-arbitrage. Two of the three Gate-0 survival requirements fail.
- **Lesson:** A magnitude edge is not a direction edge. Volatility clustering is genuine and persistent but it forecasts how big, never which way — so it cannot stand alone as a directional system, and bolting on a directional filter either imports a signal already proven dead (H2) or lets the data pick the side (curve-fit). Same landing as H8: real, filter-grade. Retain as a volatility-TIMING overlay on a separately proven directional edge, never standalone.

---

## CANDIDATE PIPELINE (untested — full thesis)

### TIER 3 — Plausible but hard to automate / weaker evidence

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
