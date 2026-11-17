---
id: computing-software.qa-testing-engineering.test-case-design.partitioning-boundaries-and-risk-based-coverage
name: partitioning-boundaries-and-risk-based-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-case-design, test-design-techniques, equivalence-partitioning, equivalence-classes, boundary-value-analysis, bva, decision-tables, state-transition-testing, pairwise-testing, combinatorial-testing, all-pairs, risk-based-testing, test-oracles, expected-results, negative-testing, edge-cases, istqb, test-coverage, requirements-coverage, black-box-testing]
level: practitioner
status: docs-checked
description: "Decide what to test: equivalence partitions, boundary values, decision tables, state transitions and pairwise combos, prioritised by risk, each case with an explicit oracle."
sources: ["https://www.istqb.org/certifications/certified-tester-foundation-level", "https://www.developsense.com/blog/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test case design: partitions, boundaries, combinations, risk

**Goal:** a small set of test cases that finds most of the defects a specification
admits, chosen deliberately rather than by intuition, each with a stated expected result.
Works for manual and automated tests alike.

Running example — *"Orders of 1–100 items. Orders of £50.00 or more ship free; members
ship free at any value. Quantity must be a whole number."*

## 1. Equivalence partitioning
Split each input into classes the system should treat the same; one test per class
is assumed representative.
| Input | Valid classes | Invalid classes |
|---|---|---|
| quantity | 1–100 | ≤0, >100, non-integer (2.5), non-numeric ("abc"), empty |
| order value | < £50.00, ≥ £50.00 | negative (if possible to reach) |
| member | yes, no | — |
Rule: combine **valid** classes freely in one test, but put **only one invalid class
per test** — otherwise the first rejection masks the second.

## 2. Boundary value analysis
Defects cluster at edges (`<` vs `<=`, off-by-one, rounding). For each ordered
partition test on and just either side of each boundary:
- quantity: **0, 1, 2** and **99, 100, 101**
- order value: **£49.99, £50.00, £50.01** (use the currency's smallest unit as the step)
Also check boundaries the spec doesn't state but the implementation has: max field
length, 32-bit integer limits, empty list, time-of-day at midnight, month end, DST change, leap day.

## 3. Decision tables for combined rules
When outcomes depend on combinations of conditions, enumerate them:
| Rule | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| member? | Y | Y | N | N |
| value ≥ £50? | Y | N | Y | N |
| **free shipping** | Y | Y | Y | N |
R1 and R2 collapse ("member → free regardless"), giving three tests. Tables expose
missing requirements: ask "what about a member whose order is refunded below £50?"

## 4. State transition testing
For workflows (order: *created → paid → shipped → delivered*, plus *cancelled*),
draw states and events, then test every valid transition once and the important
**invalid** ones: ship an unpaid order, cancel a delivered order, pay twice (double
click / retry). Invalid transitions are where real incidents hide.

## 5. Pairwise for configuration explosions
Browser (4) × OS (3) × locale (5) × payment method (4) = 240 combos. Pairwise testing assumes interaction defects usually involve few factors (an empirical rule of thumb, not a guarantee), so an all-pairs set (far fewer than 240 cases) covers every pair of values at least once. Generate it with a pairwise tool; hand-add combos known to be risky.

## 6. Prioritise by risk
Score each feature/area: **likelihood** of failure (new code, complex logic, history
of bugs, many integrations) × **impact** (money, data loss, safety, legal, number of
users). Spend deep technique (all boundaries, full decision tables) on high×high; a
single happy path and one negative case on low×low. Write the risk call down so
someone can disagree with it.

## 7. Oracles: how you know the result is right
Every case states its expected result *before* running. Sources: the spec, a
reference calculation (a spreadsheet for pricing), a previous version (regression),
consistency with similar features, invariants (totals equal sum of lines; nothing
negative). "No error appeared" is not an oracle. Where no exact oracle exists, assert
properties (property-based testing).

## Notes
The pairwise case count depends on the tool and model.

## Verify
- [ ] Every input has listed valid and invalid partitions; one invalid per test.
- [ ] Each numeric/date/length boundary has on/below/above cases.
- [ ] Combined business rules are in a decision table; gaps raised as questions.
- [ ] Invalid state transitions are tested, not just the happy path.
- [ ] Each case has a written expected result and a risk priority.

## Checked

2026-10-28. Confirmed: Worked arithmetic in the example (4 x 3 x 5 x 4 = 240); techniques are standard and carry no source-specific claims after edits. Removed: PICT/allpairspy/Hypothesis/fast-check tool names, the 20-25 case estimate and the unsupported "most bugs" claim.

Method: documentation only; no commands were run.
