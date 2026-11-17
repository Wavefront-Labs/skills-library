---
id: computing-software.qa-testing-engineering.test-case-design.each-choice-and-base-choice-coverage
name: each-choice-and-base-choice-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [base-choice-testing, each-choice-coverage, combinatorial-testing, input-space-partitioning, test-design]
level: practitioner
status: docs-checked
description: "Apply each-choice and base-choice combination criteria: minimal suites from partitions, picking a realistic base test, and when to step up to pairwise."
sources:
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Each-choice and base-choice coverage

**Goal:** cheap combination criteria below pairwise (input space partitioning).

## Each-choice (EC)
Every value (block) of every parameter appears in at least one test. Tests needed = max number of values of any parameter.
Parameters: Payment {card, paypal, voucher}, Delivery {standard, express}, Customer {new, returning}.
| # | Payment | Delivery | Customer |
|---|---|---|---|
| 1 | card | standard | new |
| 2 | paypal | express | returning |
| 3 | voucher | standard | returning |
Weakness: says nothing about which values meet; combinations are accidental.

## Base-choice (BC)
1. Pick a **base choice** per parameter: the most common or most important value (card, standard, returning).
2. Base test = all base choices.
3. Then for each parameter, vary it through every non-base value while keeping the others at base.
Tests = 1 + sum over parameters of (values - 1) = 1 + 2 + 1 + 1 = 5.
| # | Payment | Delivery | Customer |
|---|---|---|---|
| base | card | standard | returning |
| 2 | paypal | standard | returning |
| 3 | voucher | standard | returning |
| 4 | card | express | returning |
| 5 | card | standard | new |

Each failure points to one changed parameter, so diagnosis is easy. **Multiple base choice** uses several bases (e.g. one per customer segment).

## Choosing a criterion
| Criterion | Size (n params, v values) | Use |
|---|---|---|
| Each-choice | max(v) | smoke-level coverage of all values |
| Base-choice | 1 + n(v-1) | realistic flows, easy diagnosis |
| Pairwise | far fewer than all combinations; grows slowly with n | interactions between two parameters |
| All combinations | v^n | small, critical spaces only |

## Gotchas
- A bad base (rare value) wastes the suite on unrealistic tests; choose base from usage data.
- Base-choice misses interactions between two non-base values (paypal + express); add pairwise if those matter.

## Verify
Suite size matches the formula, the base test is justified by usage or risk, and every value appears at least once.

## Checked

2026-10-28 Confirmed against: arithmetic re-derived from the definitions: each-choice needs max(values) tests (3 here); base-choice needs 1 + sum(values - 1) = 1 + 2 + 1 + 1 = 5; all combinations v^n. Removed or generalised: the book citation and the pairwise size formula (the cited university page is a generic home page with no content on this).

Method: documentation only; no commands were run.
