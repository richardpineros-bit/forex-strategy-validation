# Forex Hypothesis Library — Candidate Edges

**Version:** v1.0.1
**Companion to:** Forex Strategy Validation Playbook v1.0.1
**Purpose:** A standing menu of validated-on-paper trading hypotheses to feed into the gate pipeline, plus a framework for generating new ones. Attach this to any new chat when picking the next hypothesis to run.

---

## HOW TO USE

- Each hypothesis below has passed an informal Gate 0 sniff test (it has a nameable structural reason). It still needs a *formal* Gate 0 spec before coding.
- Run them roughly in tier order — Tier 1 first. They're ranked by structural soundness and fit for hands-off, no-screen-time automation.
- Update the Status Register as each advances or dies.
- Use the Persistence Test (bottom) to vet any *new* idea before it earns a slot here.

### Ratings legend (1–5, 5 = best)
- **Structure:** how solid and well-documented the underlying inefficiency is.
- **Auto:** how cleanly it automates with zero discretion / zero screen time.
- **Life-fit:** fit for a time-poor trader (low monitoring, low decision load).
- **Fragility:** 5 = robust, 1 = fragile / easily broken by costs or crowding.

---

## TIER 1 — Strongest structural basis (start here)

### H1 — Intraday session drift ("home-vs-away" effect)
- **Claim:** Majors drift directionally by session. EUR/USD tends to weaken in European hours, strengthen in US hours.
- **Why it persists / counterparty:** Driven by recurring *non-speculative* corporate and institutional flow (hedging, fix transactions, rebalancing). The counterparty is price-insensitive — they transact for operational reasons, not profit, so they don't defend the edge. Limits to arbitrage: edge per trade is tiny and not scalable, so big capital ignores it.
- **Evidence:** Breedon & Ranaldo (2013, JMCB); documented net Sharpe ~0.7 on EUR/USD in one replication; pattern persisted in post-2007 and 2021–2023 samples.
- **Ratings:** Structure 4 · Auto 5 · Life-fit 5 · Fragility 2 (very cost-sensitive — needs cheap majors).
- **Status:** Gate 1 PASS. Currently the active hypothesis.

### H2 — Time-series trend momentum on majors
- **Claim:** A pair trending over the last N months keeps trending. Long-hold Donchian / moving-average rules.
- **Why it persists / counterparty:** Gradual information diffusion + behavioural under-reaction; also a risk premium for holding through reversals. Slow-moving money and home bias leave the trend under-exploited.
- **Evidence:** Currency momentum documented up to ~10% p.a.; hard to explain as pure risk compensation. Caveat: very-long-run (centuries) evidence is mixed.
- **Ratings:** Structure 4 · Auto 5 · Life-fit 5 · Fragility 3 (momentum crashes in sharp reversals).
- **Status:** KILLED at Gate 2 (in-sample t 0.27, no pulse; PF 1.10 pre-cost; DD −30% vs ret +2.7%). Spec H2_Trend_Momentum_Spec_v1.0.0. Not a rescue candidate — sealed OOS untouched.

### H3 — Month-end FX rebalancing flow
- **Claim:** Predictable buying/selling into the month-end benchmark fix as funds rebalance currency hedges.
- **Why it persists / counterparty:** Mechanical, calendar-driven institutional flow. Funds must rebalance to mandate regardless of price — forced, price-insensitive.
- **Evidence:** Month-end fix flows documented over decades; tied to equity/bond market moves during the month.
- **Ratings:** Structure 4 · Auto 5 · Life-fit 5 · Fragility 3 (few trades/month = slow validation).
- **Status:** Queued.

---

## TIER 2 — Real edge, more fragile or more complex

### H4 — Cross-sectional currency momentum (basket)
- **Claim:** Long the strongest currencies, short the weakest, rebalanced monthly.
- **Why it persists / counterparty:** Same momentum drivers as H2 but expressed relatively; notably *uncorrelated* to carry, so it diversifies a portfolio.
- **Evidence:** ~10% p.a. spread between past winners and losers in the literature.
- **Ratings:** Structure 4 · Auto 4 · Life-fit 4 · Fragility 3. Needs a basket (8+ currencies), more capital and plumbing than a single pair.
- **Status:** Idea — needs basket infrastructure.

### H5 — Carry trade (interest-rate differential)
- **Claim:** Long high-yield currencies, short low-yield, collect the rate differential.
- **Why it persists / counterparty:** Compensation for crash risk — UIP holds in bad times, so you're paid to bear tail risk in good times.
- **Evidence:** One of the most documented FX premia. But: bleeds slowly then crashes hard in risk-off ("pennies in front of a steamroller").
- **Ratings:** Structure 4 · Auto 4 · Life-fit 4 · Fragility 2 (dangerous tail for a small account).
- **Status:** Idea — crash-tail caution.

### H6 — London-open range breakout
- **Claim:** Trade the break of the Asian-session range as London volume floods in.
- **Why it persists / counterparty:** ~35–40% of daily turnover passes through London; the volume surge pushes price out of tight overnight ranges.
- **Evidence:** Well-known structural volume effect. But heavily crowded, and the same window produces the "Judas swing" false break that traps naive breakout traders.
- **Ratings:** Structure 3 · Auto 4 · Life-fit 4 · Fragility 2 (crowded; false-break chop).
- **Status:** Idea — crowded; don't start here.

---

## TIER 3 — Plausible but hard to automate cleanly / weaker evidence

### H7 — Liquidity-sweep reversal
- **Claim:** Price sweeps a prior high/low to grab stops, then reclaims and reverses.
- **Why it persists / counterparty:** Real mechanic — resting liquidity above/below obvious levels gets taken. But the edge lives in *how price behaves after* the sweep, which is exactly the discretionary read that resists clean rules.
- **Ratings:** Structure 3 · Auto 2 · Life-fit 2 · Fragility 2. Automation is the weak point.
- **Status:** Idea — automation-hard.

### H8 — Round-number reaction
- **Claim:** Price stalls/reverses at psychological levels (1.2000, 100.00).
- **Why it persists / counterparty:** Both retail and bank order clustering at round figures; option barriers sit there too.
- **Ratings:** Structure 3 · Auto 3 · Life-fit 3 · Fragility 3. Small and pair-dependent — better as a *filter* on another edge than a standalone strategy.
- **Status:** Idea — use as a filter.

### H9 — Volatility-compression breakout
- **Claim:** Enter on range expansion after a low-ATR squeeze.
- **Why it persists / counterparty:** Volatility clusters; compression precedes expansion. But direction at the break is not given — needs a directional filter.
- **Ratings:** Structure 3 · Auto 4 · Life-fit 4 · Fragility 2 (regime-dependent, overfit-prone).
- **Status:** Idea — overfit-prone.

### H10 — Regime-filtered mean reversion
- **Claim:** Fade stretches from a moving average, but *only* in ranging conditions.
- **Why it persists / counterparty:** Short-term overreaction corrects. But evidence conflicts — FX is described as both "efficient/mean-reverting" and "more trending than reverting." That disagreement is itself a warning.
- **Ratings:** Structure 2 · Auto 3 · Life-fit 3 · Fragility 2. Lives or dies entirely on the quality of the regime filter.
- **Status:** Idea — filter-dependent.

---

## STATUS REGISTER (keep in sync with the playbook)

| # | Hypothesis | Tier | Gate | Status |
|---|-----------|------|------|--------|
| H1 | Session drift | 1 | Gate 2 | Active |
| H2 | Trend momentum | 1 | Gate 2 | Killed |
| H3 | Month-end flow | 1 | — | Queued |
| H4 | X-sec momentum | 2 | — | Idea |
| H5 | Carry | 2 | — | Idea |
| H6 | London breakout | 2 | — | Idea |
| H7 | Liquidity-sweep | 3 | — | Idea |
| H8 | Round-number | 3 | — | Idea |
| H9 | Vol-compression breakout | 3 | — | Idea |
| H10 | Regime mean-reversion | 3 | — | Idea |

Statuses: Idea / Queued / Active / Killed / Funded.

---

## THE PERSISTENCE TEST (vet any NEW idea before it earns a slot)

Ask in order:
1. **Who is on the other side of this trade, and why?** If you can't name the loser, there is no edge.
2. **Is that counterparty price-insensitive (forced/operational) or speculative?** Forced flow = durable. Speculative = probably already arbitraged.
3. **Why hasn't it been competed away?** Valid: too small for big capital, too risky (crash tail), too slow, capacity-constrained. "Nobody knows about it" is almost never true.
4. **What would falsify it?** If you can't say, it isn't testable — and it doesn't belong here.

### Edge families, ranked by typical durability
- **Flow-based / structural (most durable):** recurring non-speculative flows — session drift, month-end fixes, index rebalancing, corporate hedging.
- **Risk-premium:** carry, value (PPP deviation), momentum. Paid for bearing real risk — durable, with crash tails.
- **Behavioural:** under/over-reaction, anchoring, round numbers. Real but small and decay-prone; best as filters.
- **Microstructure:** liquidity sweeps, breakouts, session volatility. Real mechanics but crowded and discretion-heavy.
- **Regime-conditional:** mean reversion in ranges, breakout in compression. Lives or dies on the regime filter.

### Where to mine for new hypotheses
- Academic: SSRN, Journal of Financial Economics, JMCB, BIS papers (flow/microstructure).
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

*Versioning: bump PATCH for small edits, MINOR for added/removed hypotheses, MAJOR for a re-tiering or structural rewrite. Keep the status register in sync with the playbook's Part F.*
