---
id: computing-software.qa-testing-engineering.test-case-design.decision-table-coverage-measurement
name: decision-table-coverage-measurement
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [decision-table-coverage, decision-table-testing, test-coverage, istqb, test-design]
level: practitioner
status: docs-checked
description: "Measure decision table coverage: feasible columns exercised, how collapsed columns and infeasible rules count, and minimum tests for full coverage."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decision table coverage measurement

**Goal:** report decision table coverage as defined in CTFL v4.0 4.2.3.

## Definition
Coverage items are the **columns (rules) containing feasible combinations of conditions**. Decision table coverage = columns exercised by tests / total feasible columns.
100% coverage = at least one test per feasible column.

## Counting rules
- Infeasible columns are excluded from the denominator (record why).
- A **collapsed** column (with "-" entries) counts as one coverage item; one test with any value for the don't-care condition covers it.
- If risk is high, a risk-based approach or the full (unmerged) table can be used instead; report against whichever table you used and say so.

## Example
| Rule | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Member | T | T | F | F |
| Total >= 50 | T | F | - | - |
| Coupon | - | - | T | F |
| Action | free ship | discount A | discount B | none |
4 feasible columns, tests cover R1, R2, R4 -> 3 of 4 exercised. Add a test for R3.

## In automation
Name parametrized cases by rule (`id="R3-nonmember-coupon"`) and generate the coverage report by matching IDs to the table's rule list.

## Gotchas
- Coverage of columns does not show which "-" values were tried; for don't-care conditions with risk, vary them across tests.
- Coverage is relative to the table; an incomplete table gives 100% of the wrong thing. Run a completeness check first.
- Rule-to-test mapping must be updated when the table changes; stale IDs give false coverage.

## Verify
Coverage figure states numerator, denominator, excluded infeasible columns, and whether columns were collapsed or expanded.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL v4.0.1 syllabus (section 4.2.3): coverage items are the columns containing feasible combinations of conditions, coverage is exercised columns divided by total feasible columns, a dash means the condition value is irrelevant, infeasible columns can be deleted, columns can be merged when some conditions do not affect the outcome, and a minimized table or a risk-based approach reduces the rules to exercise. Removed: the claim that expanding collapsed columns is a syllabus option.
Method: documentation only; no commands were run.
