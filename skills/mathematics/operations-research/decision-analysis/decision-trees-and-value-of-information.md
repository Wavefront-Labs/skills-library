---
id: mathematics.operations-research.decision-analysis.decision-trees-and-value-of-information
name: decision-trees-and-value-of-information
category: mathematics
field: operations-research
product: decision-analysis
tags: [operations-research, decision-analysis, decision-tree, expected-value, expected-monetary-value, emv, rollback, utility-theory, risk-aversion, certainty-equivalent, value-of-information, evpi, evsi, bayes-rule, sensitivity-analysis, tornado-diagram, multi-criteria-decision-analysis, mcda, swing-weighting, influence-diagram, decision-under-uncertainty]
level: practitioner
status: verified
description: "Structure a decision under uncertainty: build and roll back a decision tree, apply utility for risk attitude, compute EVPI/EVSI to price information, and run sensitivity checks."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decision trees and value of information

**Goal:** make a choice under uncertainty explicit — options, chances, payoffs — and
know how much it is worth paying to reduce the uncertainty before deciding.

## 1. Frame the decision
- **Decision** and the real alternatives (include "do nothing" and "wait / test first").
- **Uncertainties** that change the outcome, with mutually exclusive, exhaustive states.
- **Value measure** — usually net present value in money; for non-monetary aims see
  section 6.
Draw in time order: squares = decisions, circles = chance nodes, triangles = end payoffs.

## 2. Roll back
Work right to left: at a chance node take the probability-weighted average; at a
decision node take the best branch.
Example — launch a product (cost 2M):
- Strong demand (p = 0.4): revenue 6M → net 4M
- Weak demand (p = 0.6): revenue 1M → net −1M
EMV(launch) = 0.4·4 + 0.6·(−1) = 1.0M; EMV(don't) = 0. Launch.

## 3. Value of information
**EVPI** (expected value of perfect information): the most you'd ever pay for a
perfect forecast.
- With perfect info: strong → launch (4M), weak → don't (0). EV = 0.4·4 + 0.6·0 = 1.6M.
- EVPI = 1.6 − 1.0 = **0.6M**. Any study costing more is not worth it.
**EVSI** for an imperfect test (a market survey):
1. Specify its accuracy: P(positive | strong) = 0.8, P(positive | weak) = 0.3.
2. P(positive) = 0.8·0.4 + 0.3·0.6 = 0.50.
3. Bayes: P(strong | positive) = 0.32/0.50 = 0.64; P(strong | negative) = 0.08/0.50 = 0.16.
4. After positive: EMV(launch) = 0.64·4 + 0.36·(−1) = 2.2 → launch.
   After negative: 0.16·4 + 0.84·(−1) = −0.2 → don't launch (0).
5. EV with survey = 0.5·2.2 + 0.5·0 = 1.1M. **EVSI = 1.1 − 1.0 = 0.1M.**
Survey worth buying only if it costs < 0.1M. Information has value only if some
result would **change the decision**; if not, EVSI = 0.

## 4. Risk attitude: utility
EMV assumes risk neutrality — fine for small bets relative to the organisation's size.
For large stakes use a utility function, e.g. exponential u(x) = 1 − e^(−x/R), with
**risk tolerance R** roughly the sum at which a 50/50 gamble of +R / −R/2 feels
just acceptable (a common elicitation; treat as approximate).
- Roll back expected **utility**, then convert to a **certainty equivalent**:
  CE = −R·ln(1 − EU).
- CE < EMV; the difference is the risk premium.

## 5. Sensitivity analysis
- **One-way:** vary each probability and payoff across a plausible range; find the
  **breakeven** point where the preferred choice switches. Example: launch is preferred
  while p(strong) > 0.2 (solve 4p − (1 − p) = 0).
- **Tornado diagram:** bars for each input's swing in EMV, largest at top — tells you
  where better estimates matter.
- Elicit probabilities with care: ask for ranges, use reference classes, and beware
  anchoring and overconfidence.

## 6. Multiple criteria (MCDA)
When value isn't one currency (cost, safety, environmental impact):
1. Define criteria that are independent and measurable.
2. Score options 0–100 on each (worst to best in the considered range).
3. **Swing weighting:** rank the swings from worst to best on each criterion, give the
   most important swing 100, others relative — weights depend on ranges, not abstract "importance".
4. Weighted sum, then sensitivity on the weights.

Every number in sections 2, 3 and 5 was recomputed (EMV 1.0M, EVPI 0.6M, P(positive) 0.50, posteriors 0.64 and 0.16, EV with survey 1.1M, EVSI 0.1M, breakeven p = 0.2); with exponential utility a +R / -R/2 gamble has a certainty equivalent of about -0.008R, close to indifference, as the skill says.

## Tools
Spreadsheet trees for small problems; PrecisionTree, TreeAge, Analytica, or Python
(write the rollback recursively) for larger ones. Influence diagrams compress large trees.

## Gotchas
- Missing alternatives (especially "test first" or "stage the investment") are the
  biggest error — not arithmetic.
- Probabilities at a chance node must sum to 1; outcomes must be exclusive.
- Discount multi-year payoffs before rolling back.
- Double counting: if a payoff already includes a cost, don't subtract it again at a branch.

## Verify
- [ ] All alternatives, including wait/test/stage, appear.
- [ ] Chance-node probabilities sum to 1; Bayes revision done correctly for tests.
- [ ] Rollback reproduces by hand on the top branches.
- [ ] EVPI computed; any information purchase costs less than its EVSI.
- [ ] Breakeven values and a tornado diagram identify the decisive inputs.
