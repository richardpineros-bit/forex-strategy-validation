# Forex Strategy Validation Playbook — Master Reference

**Version:** v1.0.9
**Purpose:** A reusable, gate-based pipeline for taking a trading idea from "hunch" to "fundable automated strategy" without falling into the curve-fitting trap. Built for a time-constrained trader automating away from manual execution.

**Changelog**
- v1.0.9 - H9 (volatility-compression breakout) KILLED at Gate 0, standalone. Not a feasibility death - squeeze-then-expand IS observable on daily ATR (ATR(n) low vs its own history, then a bar breaking the squeeze range), so the H3/H8 granularity excuse explicitly does not apply; killed on the edge story. No pre-registered direction survives theory: ARCH/GARCH volatility clustering forecasts MAGNITUDE not sign; HTF-trend continuation imports the H2 trend-momentum signal already dead at Gate 2; dealer-gamma is a magnitude argument (long gamma suppresses the range, short gamma amplifies the break), not a direction; letting the backtest pick the winning side is the forbidden multiple-testing curve-fit. Counterparty is speculative and adaptive (range traders, mean-reversion algos, long-gamma dealers run over on expansion) = H6 disease, crowded, Judas-swing false breaks; no daily-scale limits-to-arbitrage. A magnitude edge is not a directional edge. Real but filter-grade; retain as a volatility-timing overlay on a separate proven directional edge, never standalone. No code. Tier-3 queue now H10 only. Companion library v1.2.3.
- v1.0.8 - H8 (round-number reaction) KILLED at Gate 0, standalone. Feasibility on the box's daily OHLC decided it: the strict pierce-and-reclaim proxy (closest to Osler 2003) fires on ~0.1% of bars (untestable, ~7 events/pair in 20y); the loose approach-and-reject proxy has frequency (~24% of bars) but a control test rejects at arbitrary non-round levels at the same ~21% rate - it measures generic daily bar shape, not a round-number reaction. The one durable strand (bank option-barrier defence - a semi-forced counterparty, better than H6/H7's speculative one) is unlocatable without intraday data + an options book. H3 disease (intraday mechanism dilutes daily) confirmed numerically. Real but filter-grade; retain as confluence, never standalone. No code. Tier-3 queue now H9-H10. Companion library v1.2.2.
- v1.0.7 - H7 (liquidity-sweep) KILLED at Gate 0. Re-scoped from the intraday sweep (no intraday data on box) to a daily failed-breakout reversal, which IS mechanically definable on daily OHLC (reclaim = close back inside the swept level) - so not a Gate 1 death. Killed on the edge story: no forced counterparty + no daily-scale limits-to-arbitrage; stacks the H3 disease (Osler stop-cascade is intraday, dilutes on a daily hold) and the H6 disease (speculative/predator counterparty adapts). No code. Tier-3 queue now H8-H10.
- v1.0.6 - Cosmetic sync only (no register change). Back-filled the missing v1.0.4/v1.0.5 changelog entries (reconstructed from Part F notes) and updated the Part G quick-start reference to the current version. Companion library is now v1.2.0.
- v1.0.5 - H6 (London breakout) KILLED at Gate 0 on feasibility: no intraday data on box; weakest persistence story in the queue (mechanism supports volatility not direction; predator stop-hunt counterparty, not forced flow). No code written. Tier-2 queue exhausted.
- v1.0.4 - H4 (x-sec momentum) and H5 (carry) KILLED at Gate 2 in-sample. H4: n152, mean -0.0835%/mo, t -0.449, wrong sign, Sharpe -0.13, DD -29%. H5: mean +0.12%/mo, t 0.62 (insignificant), Sharpe 0.17, DD -30% - correct sign but t<1 = no significant edge. No rescue on either.
- v1.0.3 - H3 (month-end flow) KILLED at Gate 2 (pooled core-4 t -0.16, mean -0.91bps, 2/4 pairs positive; winsorising the SNB outlier did not change it). Corrected stale H1 register row to Killed. All Tier-1 ideas now exhausted.
- v1.0.2 — H2 (trend momentum) KILLED at Gate 2 (in-sample t 0.27, no pulse). Status register updated.
- v1.0.1 — Added the "pre-register direction from theory" principle (Part A, Gate 0, Part D). Updated status register: H1 advanced to Gate 1.
- v1.0.0 — Initial pipeline, hypothesis library, worked Gate 0, generation framework.

---

## HOW TO USE THIS DOCUMENT

1. **One hypothesis per chat.** Start a fresh chat for each hypothesis to keep context clean.
2. **Paste the Quick-Start block** (Part G) into the new chat, fill in which hypothesis and which gate you're on.
3. **Run one gate at a time.** A hypothesis only advances if it passes. Failing is normal and cheap.
4. **Update the Status Register** (Part F) after each session so you always know where every idea sits.
5. **Killing on a spreadsheet is free. Killing with funded capital is not.** That is the entire point of this process.

---

## PART A — CORE PHILOSOPHY (THE RULES THAT DON'T BEND)

- **Hypothesis before code.** If you cannot name *why* an edge exists in one paragraph, there is nothing worth automating.
- **The enemy is curve-fitting.** Test enough variations against history and you will *always* find one that looks profitable. That is selection bias fitting noise, not edge.
- **Pre-register direction from theory; let data confirm or kill.** When research gives a directional prior (e.g. "short EUR/USD in EU hours"), commit to it *before* testing. Trying both directions and keeping the winner is multiple-testing curve-fitting. A theory-driven prior the data then confirms is far stronger than a direction the data was allowed to pick.
- **Fewer parameters = more trust.** Every tunable knob is another way to fit noise. Target under 5 free parameters.
- **In-sample is for building. Out-of-sample is for truth.** A strategy that only shines on data it was built on is fitted and will die live.
- **Edge must survive costs.** Spread, slippage, commission and swap kill most "profitable" systems. Frictionless profit is fantasy.
- **Flat risk during validation. Micro-size before funding. Scale gradually after.** No exceptions.
- **You cannot automate an edge you have not proven.** Automating an unproven edge just loses money faster and more consistently.
- **State what would falsify the idea, up front.** If you can't define what would prove it wrong, it's not testable.

---

## PART B — THE GATE PIPELINE

A strategy advances only by passing each gate in order. Each gate lists: **Purpose**, **Do**, **PASS criteria**, **On FAIL**, and **Do NOT**.

### GATE 0 — Hypothesis (paper, no code)
- **Purpose:** Establish that a real, nameable inefficiency exists before spending any effort.
- **Do:** Write (a) a one-paragraph hypothesis, (b) the named inefficiency and *why it persists*, (c) who is on the other side of the trade and why they don't care about losing the edge, (d) a rough rule skeleton, (e) the falsification condition. **If research provides a directional prior, pre-register that direction here** — it is fixed input, not something the backtest gets to choose.
- **PASS:** You can name the structural reason AND identify a price-insensitive / non-speculative counterparty OR a documented limits-to-arbitrage reason it survives.
- **On FAIL:** Discard. Do not proceed to code "to see if it works." ~80% of ideas die here. Good.
- **Do NOT:** Accept "indicator X crosses indicator Y" as a hypothesis. That is a rule, not a reason.

### GATE 1 — Strict Rule Set (paper/pseudocode)
- **Purpose:** Convert the idea into unambiguous, discretion-free rules.
- **Do:** Specify exact entry, exit, stop, target, position sizing, filters, and trading hours. Lock the primary specification (pre-registered values from theory where available); list alternatives only as Gate 5 robustness checks, not as a Gate 2 optimisation search. Count free parameters. Define the in-sample/out-of-sample split rule.
- **PASS:** Every decision is mechanical (a machine could execute it with no judgement). Free parameters < 5.
- **On FAIL:** Tighten until zero discretion remains. If discretion can't be removed, it can't be automated — kill or re-scope.
- **Do NOT:** Leave "enter on a good setup" or any phrase requiring a human eye. Don't smuggle in an optimisation search dressed up as "candidate windows."

### GATE 2 — In-Sample Backtest (~60% of history)
- **Purpose:** Confirm the logic runs and the edge shows a pulse on the build data.
- **Do:** Code the rules. Backtest on the *first ~60%* of available history. Record trade count, win rate, profit factor, max drawdown, expectancy, and the significance (t-stat) of the core signal.
- **PASS:** Positive expectancy with a believable (not spectacular) curve, the pre-registered direction is the correct sign, and enough trades to mean something (aim 100+; 30 absolute floor).
- **On FAIL:** If logic is broken, fix and re-run. If edge is genuinely absent or the wrong sign, kill.
- **Do NOT:** Optimise heavily here. Be suspicious of anything that looks too good — that's the fitting tell.

### GATE 3 — Out-of-Sample / Walk-Forward (~40% held back)
- **Purpose:** The real test. Does the edge survive on data it has never seen?
- **Do:** Run the *same frozen rules* on the held-back ~40%. Optionally walk-forward across rolling windows.
- **PASS:** Out-of-sample expectancy holds at a meaningful fraction of in-sample (rough guide: keeps >50% of in-sample edge). Direction/sign does NOT flip.
- **On FAIL:** It was fitted. Kill it. Do not re-optimise on the out-of-sample data — that destroys the test.
- **Do NOT:** Peek at out-of-sample during the build. Once you optimise on it, it's no longer out-of-sample.

### GATE 4 — Realistic Costs
- **Purpose:** Confirm the edge survives the real world, not a frictionless model.
- **Do:** Re-run with realistic spread, slippage, commission and overnight swap baked in. Use *your* broker's actual numbers.
- **PASS:** Still net-positive expectancy after all costs, with comfortable margin (not break-even).
- **On FAIL:** Kill, or restrict to cheaper pairs / longer holds where costs matter less.
- **Do NOT:** Use idealised spreads. Many strategies are only profitable for free.

### GATE 5 — Robustness
- **Purpose:** Confirm the edge is real, not a lucky parameter on a lucky window.
- **Do:** Three checks — (a) **Parameter sensitivity:** nudge each parameter +/-20%; profit should degrade gracefully, not collapse. (b) **Regime test:** does it survive trending AND ranging periods, or only one lucky stretch? (c) **Risk-of-ruin / drawdown:** model the worst run; can you stomach it without bailing?
- **PASS:** Profitable across a *plateau* of nearby parameters (not a single spike), survives multiple regimes, and worst-case drawdown is survivable at your risk size.
- **On FAIL:** Fragile. Kill, or simplify until robust.
- **Do NOT:** Trust a knife-edge optimum. Robust edges are broad, not precise.

### GATE 6 — Forward Test, Micro-Size
- **Purpose:** Catch real-world execution gaps a backtest can't model (fills, gaps, broker behaviour).
- **Do:** Deploy live at the *smallest size the broker allows*, for 2-3 months minimum. This is your only "spend money to test" step — bounded to lunch money.
- **PASS:** Live results track the backtest within reason. No nasty execution surprises.
- **On FAIL:** Diagnose the gap (slippage, fills, latency). Fix and re-test, or kill.
- **Do NOT:** Skip straight to real size. Backtests lie about execution.

### GATE 7 — Fund & Scale
- **Purpose:** Deploy real capital responsibly.
- **Do:** Fund only after 0-6 pass. Start small, scale gradually as live data confirms. Keep monitoring vs the backtest baseline; degradation = pull back.
- **PASS:** This is the destination, not a test.
- **Do NOT:** Jump to full size on day one. Scale in steps.

---

## PART C — HYPOTHESIS LIBRARY

Tiered by structural soundness and fit for fully-automated, no-screen-time trading.

### Tier 1 — Strongest structural basis
1. **Intraday session drift / "home-vs-away" seasonality** — majors drift directionally by session, driven by recurring non-speculative corporate/institutional flow. Documented net Sharpe ~0.7 on EUR/USD in one study. *Best life-fit: pure time rules, no screen time.* Fragile to costs — needs cheap majors.
2. **Time-series trend momentum on majors** — a trending pair keeps trending; long-hold Donchian/MA rules. Documented currency momentum up to ~10% p.a.; hard to explain as pure risk. Low-frequency, hands-off. Risk: momentum crashes; very-long-run evidence mixed.
3. **Month-end FX rebalancing flow** — predictable buying/selling into the month-end fix as funds rebalance hedges. Mechanical calendar flow. Clean to automate. Slow data accumulation (few trades/month).

### Tier 2 — Real edge, more fragile or complex
4. **Cross-sectional currency momentum (basket)** — long strongest, short weakest currencies, monthly rebalance. ~10% p.a. spread; uncorrelated to carry. Needs a basket (8+ currencies), more capital/plumbing.
5. **Carry trade (rate differential)** — long high-yield, short low-yield. Well documented but bleeds slowly then crashes in recessions (UIP holds in bad times). Dangerous tail for a small account.
6. **London-open range breakout** — break of Asian range as London volume (~35-40% of daily turnover) floods in. Objective, automatable. Crowded; "Judas swing" false breaks chop the naive version.

### Tier 3 — Plausible but hard to automate cleanly / weaker
7. **Liquidity-sweep reversal** — sweep prior high/low then reclaim. Real mechanic, but the edge is in *how price behaves after* the sweep — exactly the discretionary read that resists clean automation.
8. **Round-number reaction** — stalls/reversals at psychological levels. Real but small and pair-dependent. Better as a filter than a standalone edge.
9. **Volatility-compression breakout** — enter on range expansion after a low-ATR squeeze. Automatable but regime-dependent and over-fit-prone.
10. **Regime-filtered mean reversion** — fade stretches from a mean, only in ranges. Evidence conflicts (FX called both "efficient/mean-reverting" and "more trending than reverting"). Lives or dies on the regime filter.

**Recommended order:** #1 first (best constraint fit), #2 second (uncorrelated, equally hands-off). Avoid starting with #6/#7 — most crowded and most discretion-prone.

---

## PART D — WORKED GATE 0 (QUALITY BAR): HYPOTHESIS #1, SESSION DRIFT

This is the standard every Gate 0 should meet. (Full standalone spec: H1_Session_Drift_Gate0_Spec.)

**(a) Hypothesis (one paragraph):**
Major FX pairs (starting with EUR/USD) exhibit a small but persistent intraday directional drift that depends on the trading session. The drift is produced by recurring, time-clustered, non-speculative flows — corporate hedging during home-currency business hours, reserve-manager and index-fund rebalancing, and benchmark "fix" transactions — that recur at predictable clock times. Because these participants transact for operational reasons rather than to profit, the drift is not competed away the way a speculative edge would be. (Source: Breedon & Ranaldo 2013, JMCB — currencies depreciate during local business hours.)

**(b) Named inefficiency & why it persists:**
Efficient-market / uncovered-interest-parity logic says no predictable intraday drift should exist. It persists because the *marginal* flow at these times is price-insensitive: a corporate treasurer hedging receivables or a fund rebalancing to a benchmark must transact regardless of level. The arbitrage force that would normally flatten the drift is weak because the edge per trade is tiny, the holding window is short, and it is not scalable to institutional size — classic **limits to arbitrage**. Big players can't be bothered; that's precisely why it survives for a low-cost retail trader.

**(c) Who is on the other side, and why they don't care:**
Corporates, reserve managers, and index funds — executing for operational/mandate reasons, not profit. They are not trying to win the trade, so they don't defend the edge. That is what makes it durable.

**(d) Rule skeleton (to harden in Gate 1):**
- Universe: EUR/USD first (tightest spread); later USD/JPY, GBP/USD.
- Signal: **time-of-day only.** Enter at session boundary X, exit at session boundary Y. No indicators, no discretion.
- **Direction: pre-registered from the Breedon-Ranaldo home-away effect** — short EUR/USD in European hours, long in US hours. The in-sample test confirms or kills this direction. We do NOT try both directions and keep the winner.
- Risk: flat/fixed during validation.
- Free parameters to keep minimal: entry time, exit time, pair.

**(e) Falsification condition (define up front):**
The hypothesis is dead if ANY of: the drift's direction is not the pre-registered sign across the in-sample period; the sign flips out-of-sample; or the edge does not survive realistic spread on a cheap major. Pre-committing to these kill-conditions is what stops curve-fitting later.

**Gate 0 verdict: PASS.** Named inefficiency, price-insensitive counterparty, documented persistence, pre-registered direction, explicit falsification. Proceed to Gate 1.

---

## PART E — HYPOTHESIS-GENERATION FRAMEWORK (FOR NEW IDEAS)

Use this to generate the *next* hypothesis instead of grabbing a random indicator combo.

### The persistence test — ask in order:
1. **Who is on the other side of this trade, and why?** If you can't name the loser, there is no edge.
2. **Is that counterparty price-insensitive (forced/operational) or speculative?** Forced flow = durable edge. Speculative = likely already arbitraged.
3. **Why hasn't it been competed away?** Valid answers: too small to matter to big capital; too risky (crash tail); too slow; capacity-constrained. "Nobody knows about it" is almost never true.
4. **What would falsify it?** If you can't say, it isn't testable.

### Edge families (ranked by typical durability):
- **Flow-based / structural (most durable):** non-speculative recurring flows — session drift, month-end fixes, index rebalancing, corporate hedging. Survives because the counterparty doesn't care.
- **Risk-premium:** carry, value (PPP deviation), momentum factors. Compensation for bearing real risk — durable, but with crash tails.
- **Behavioural:** under/over-reaction, anchoring, round numbers. Real but small and decay-prone; best as filters.
- **Microstructure:** liquidity sweeps, breakouts, session volatility. Real mechanics but crowded and discretion-heavy.
- **Regime-conditional:** mean reversion in ranges, breakout in compression. Lives or dies on the regime filter quality.

### Where to mine for new hypotheses:
- Academic: SSRN, Journal of Financial Economics, JMCB, BIS papers (especially flow/microstructure).
- Quant libraries: Quantpedia strategy database, RobotWealth, QuantRocket.
- Structural data: BIS Triennial Survey (where the volume actually is), broker/COT positioning.
- **Your own journal:** where do *you* historically have positive expectancy? An edge you already have is the cheapest to validate.

### Blank Gate 0 template (copy for each new idea):
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

## PART F — STATUS REGISTER (UPDATE EACH SESSION)

| # | Hypothesis | Tier | Current Gate | Status | Notes |
|---|-----------|------|--------------|--------|-------|
| 1 | Session drift | 1 | Gate 3 | Killed | Passed in-sample (t 3.93), died OOS (t 0.20, PF 1.01). OOS is the only truth. |
| 2 | Trend momentum | 1 | Gate 2 | Killed | In-sample t 0.27, PF 1.10, DD−30% vs ret +2.7%. Spec v1.0.0. No rescue. |
| 3 | Month-end flow | 1 | Gate 2 | Killed | Pre-registered dir wrong-signed/absent pooled core-4 (t -0.16, mean -0.91bps, 2/4 pairs +). Daily candles dilute the intraday fix effect. Spec v1.0.0. No rescue. |
| 4 | X-sec momentum | 2 | Gate 2 | Killed | In-sample n152, mean -0.0835%/mo, t -0.449, wrong sign (faint reversal tilt), Sharpe -0.13, DD -29%. No rescue. |
| 5 | Carry | 2 | Gate 2 | Killed | In-sample mean +0.12%/mo, t 0.62 (insignificant), Sharpe 0.17, DD -30%. Correct sign but t under 1 = no significant edge = kill. OOS sealed. |
| 6 | London breakout | 2 | Gate 0 | Killed | KILLED on feasibility. No intraday data on box and weakest persistence story in the queue (mechanism supports volatility not direction; predator stop-hunt counterparty). Not worth sourcing hourly data to test the shakiest Gate 0. No code written. |
| 7 | Liquidity-sweep | 3 | Gate 0 | Killed | Re-scoped from intraday sweep (no intraday data) to daily failed-breakout. Definable on daily OHLC (reclaim = close back inside) so NOT a Gate 1 death. KILLED Gate 0 on edge story: no forced counterparty, no daily-scale limits-to-arb; H3 disease (Osler cascade intraday, dilutes daily) + H6 disease (speculative/predator counterparty adapts). No code. |
| 8 | Round-number | 3 | Gate 0 | Killed | KILLED standalone on feasibility. Daily OHLC can't isolate the effect: strict pierce-reclaim proxy ~0.1% of bars (untestable); loose approach-reject proxy fires at arbitrary non-round levels at the same rate (~24% round vs ~21% arbitrary) = generic bar shape, not round-number reaction. Durable strand (option-barrier defence) unlocatable without intraday + options book. H3 disease. Filter-grade only. No code. |
| 9 | Vol-compression breakout | 3 | Gate 0 | Killed | KILLED standalone on the edge story, NOT feasibility (squeeze-then-expand is observable on daily ATR). No theory-given direction: HTF-trend continuation imports the dead H2 signal; gamma/ARCH are magnitude not sign; letting data pick the side = curve-fit. Counterparty speculative/adaptive (range/mean-rev faders, long-gamma dealers) = H6 disease; no daily limits-to-arb. A magnitude edge is not a direction edge. Filter-grade only. No code. |
| 10 | Regime mean-reversion | 3 | — | Idea | Filter-dependent |

Statuses: Idea / Queued / Active / Killed / Funded.

---

## PART G — QUICK-START BLOCK FOR A NEW CHAT

Paste this into a fresh chat and fill the blanks:

```
I'm running a forex strategy through my validation pipeline (playbook v1.0.9).

Hypothesis: #__ <name>
Current gate: Gate __
Previous gate result: <summary of what passed / the numbers>
Goal for this session: run Gate __ and give me a clear PASS or KILL.

Reminders:
- One hypothesis, one gate at a time.
- Discretion-free, <5 free parameters, flat risk in validation.
- Direction pre-registered from theory, not picked by the data.
- Out-of-sample is truth; don't optimise on it.
- Must survive realistic costs.
- Be blunt. Kill it if it deserves killing.
```

---

*Versioning: bump PATCH for small edits, MINOR for added sections/hypotheses, MAJOR for a structural rewrite. Filename carries the version (e.g. Forex_Strategy_Validation_Playbook_v1.0.2.md).*
