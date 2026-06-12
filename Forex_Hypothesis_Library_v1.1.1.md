# Forex Hypothesis Library — Candidate Edges & Resolved Results

**Version:** v1.1.1
**Companion to:** Forex Strategy Validation Playbook v1.0.3
**Purpose:** A lean ledger of trading hypotheses. For *resolved* ideas: the result and why it worked or didn't — so a dead idea is never re-tested. For *untested* ideas: a full thesis ready to feed into the gate pipeline.

**Changelog**
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
| H4 | X-sec momentum | 2 | — | Idea |
| H5 | Carry | 2 | — | Idea |
| H6 | London breakout | 2 | — | Idea |
| H7 | Liquidity-sweep | 3 | — | Idea |
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

---

## CANDIDATE PIPELINE (untested — full thesis)

### TIER 2 — Real edge, more fragile or complex

#### H4 — Cross-sectional currency momentum (basket)
- **Claim:** Long strongest currencies, short weakest, monthly rebalance.
- **Why it persists / counterparty:** Momentum drivers expressed relatively; uncorrelated to carry, so it diversifies.
- **Evidence:** ~10% p.a. winner-minus-loser spread in the literature. (This is the result H2 mistakenly borrowed.)
- **Ratings:** Structure 4 · Auto 4 · Life-fit 4 · Fragility 3. Needs a basket (8+ currencies), more capital and plumbing.
- **Status:** Idea — needs basket infrastructure.

#### H5 — Carry trade (interest-rate differential)
- **Claim:** Long high-yield, short low-yield; collect the differential.
- **Why it persists / counterparty:** Compensation for crash risk — UIP holds in bad times, so you're paid to bear the tail in good times.
- **Evidence:** Heavily documented premium. But bleeds slowly then crashes in risk-off ("pennies in front of a steamroller").
- **Ratings:** Structure 4 · Auto 4 · Life-fit 4 · Fragility 2 (dangerous tail for a small account).
- **Status:** Idea — crash-tail caution.

#### H6 — London-open range breakout
- **Claim:** Trade the break of the Asian range as London volume floods in.
- **Why it persists / counterparty:** ~35–40% of daily turnover passes through London; the surge pushes price out of tight overnight ranges.
- **Evidence:** Well-known volume effect. But crowded, and the same window produces the "Judas swing" false break.
- **Ratings:** Structure 3 · Auto 4 · Life-fit 4 · Fragility 2 (crowded; false-break chop).
- **Status:** Idea — crowded; don't start here.

### TIER 3 — Plausible but hard to automate / weaker evidence

#### H7 — Liquidity-sweep reversal
- **Claim:** Price sweeps a prior high/low to grab stops, then reclaims and reverses.
- **Why it persists / counterparty:** Real mechanic — resting liquidity gets taken. But the edge lives in *how price behaves after* the sweep — the discretionary read that resists clean rules.
- **Ratings:** Structure 3 · Auto 2 · Life-fit 2 · Fragility 2. Automation is the weak point.
- **Status:** Idea — automation-hard.

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
