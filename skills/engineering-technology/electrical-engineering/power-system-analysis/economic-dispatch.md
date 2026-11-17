---
id: engineering-technology.electrical-engineering.power-system-analysis.economic-dispatch
name: economic-dispatch
category: engineering-technology
field: electrical-engineering
product: power-system-analysis
tags: [economic-dispatch, electrical-engineering, incremental-cost, lambda-iteration, loss-penalty-factors, power-system-analysis, unit-commitment]
level: practitioner
status: draft
description: "Dispatch generators at equal incremental cost with limits and loss penalty factors, and understand the unit commitment layer."
sources:
  - "https://standards.ieee.org/"
  - "https://www.ncees.org/engineering/pe/electrical-computer/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Economic dispatch and unit commitment

1. Cost curves `F_i(P) = a + b P + c P^2`; incremental cost `dF/dP = b + 2 c P = lambda` for all unconstrained units.
2. Solve `sum P_i = P_demand`. Example: C1 = 500 + 5.3 P + 0.004 P^2, C2 = 400 + 5.5 P + 0.006 P^2, demand 800 MW: `lambda = 9.22`, P1 = 490 MW, P2 = 310 MW.
3. **Limits:** fix units at their min or max and re-solve for the others; iterate on lambda (bisection) until the power balance is met.
4. **Losses:** use penalty factor `L_i = 1 / (1 - dP_loss/dP_i)` and equalise `lambda_i L_i` ; loss coefficients come from a load-flow or B-matrix.
5. **Unit commitment:** adds on/off decisions with start-up costs, minimum up/down times and ramp limits; solved by priority lists, dynamic programming or mixed-integer programming, not by the dispatch formula.

**Verify:** at the solution all unconstrained units show the same incremental cost and total generation equals demand plus losses.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
