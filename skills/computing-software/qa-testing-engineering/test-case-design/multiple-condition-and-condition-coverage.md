---
id: computing-software.qa-testing-engineering.test-case-design.multiple-condition-and-condition-coverage
name: multiple-condition-and-condition-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [multiple-condition-coverage, condition-coverage, white-box-testing, decision-coverage, condition-decision-coverage, istqb-tta]
level: practitioner
status: draft
description: "Understand and apply condition, condition/decision and multiple condition coverage, their test counts, how they relate to MC/DC, and when each is worth the cost."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Condition and multiple condition coverage

**Goal:** pick a condition-level coverage criterion that fits the risk. CTAL-TTA v4.0 2.2-2.3.

## Criteria for decision `if (A && B)`
| Criterion | Requirement | Min tests (2 conditions) |
|---|---|---|
| Decision (branch) | decision T and F | 2 |
| Condition | each condition T and F (decision may not change) | 2 (e.g. TF, FT: both decisions F!) |
| Condition/decision | both of the above | 2-3 |
| MC/DC | each condition independently flips outcome | 3 (TT, FT, TF) |
| Multiple condition | all combinations | 4 (2^n) |

Condition coverage alone can leave the decision always false: weaker than it sounds.

## Multiple condition coverage
All 2^n combinations: 3 conditions = 8, 6 conditions = 64. With short-circuit languages, many combinations are not evaluated (`A` false means `B` is never evaluated), so the set of *evaluated* combinations is smaller; tools differ in counting.

## When to use what
- Branch coverage: default target for business code.
- MC/DC: safety-critical, or complex Boolean expressions in critical paths (`mcdc-coverage`).
- Multiple condition: small decisions with high criticality where full combinations are cheap (<= 3 conditions).

## Measuring
coverage.py and JaCoCo measure branches (not conditions). For conditions: gcc `-fcondition-coverage`, Clang MC/DC, commercial tools, or derive by hand with a truth table for critical decisions.

## Gotchas
- Refactoring compound conditions into separate `if`s turns condition coverage into branch coverage that tools can measure.

## Verify
Truth table per critical decision with the chosen criterion's required rows linked to tests.
