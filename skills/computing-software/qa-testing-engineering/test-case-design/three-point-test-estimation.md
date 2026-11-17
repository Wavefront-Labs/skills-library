---
id: computing-software.qa-testing-engineering.test-case-design.three-point-test-estimation
name: three-point-test-estimation
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [three-point-estimation, test-estimation, pert, estimation-uncertainty, istqb]
level: practitioner
status: draft
description: "Use three-point (PERT) estimation for test effort: optimistic, most likely and pessimistic values, expected value and standard deviation, and how to communicate ranges."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Three-point estimation

**Goal:** estimates that state uncertainty honestly. ISTQB CTFL v4.0 5.1.4.

## Formula
For each task: optimistic **a**, most likely **m**, pessimistic **b**.
- Expected E = (a + 4m + b) / 6
- Standard deviation SD = (b - a) / 6
Sum E over tasks for the total; total SD = sqrt(sum of SD^2) if tasks are independent.

## Example
| Task | a | m | b | E | SD |
|---|---|---|---|---|---|
| Test design | 4 | 6 | 14 | 7.0 | 1.67 |
| Automation | 10 | 15 | 30 | 16.7 | 3.33 |
| Execution + retest | 6 | 10 | 22 | 11.3 | 2.67 |
| Total | | | | 35.0 | 4.59 |

Report: "about 35 days; ~84% chance within 39.6 days (E + 1 SD), ~98% within 44 (E + 2 SD)".
CTFL's syllabus example uses E +/- SD as the range.

## Getting the inputs right
- Pessimistic should reflect real risks: environment late, unstable build, high defect rate causing retest cycles.
- Use historical data for m where possible.

## Gotchas
- Giving management only E invites treating it as a commitment; always give the range.
- Correlated risks (same unstable environment affects all tasks) make the sqrt-sum too optimistic.

## Verify
Actuals fall within the stated range most of the time; if always above E + SD, your pessimistic values are too low.
