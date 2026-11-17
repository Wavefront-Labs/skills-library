---
id: computing-software.qa-testing-engineering.test-case-design.collapsing-decision-tables
name: collapsing-decision-tables
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [collapsed-decision-table, decision-tables, dont-care-conditions, rule-minimisation, istqb]
level: practitioner
status: docs-checked
description: "Build a full decision table, then collapse it with don't-care entries to remove infeasible and redundant rules while keeping full rule coverage."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collapsing decision tables

**Goal:** fewest test cases that still cover every distinct business rule. ISTQB CTFL v4.0 4.2.3.

## Steps
1. List conditions (inputs) and actions (outputs).
2. Full table: 2^n columns for n Boolean conditions.
3. Fill actions per column from the spec; mark **infeasible** combinations (cannot occur) and remove them.
4. **Collapse**: if two columns differ in only one condition and have identical actions, merge them and mark that condition `-` (don't care).
5. Repeat until no more merges. Each remaining column is a rule = one test.

## Example: loan fee waiver
Conditions: C1 existing customer, C2 loan > 10k, C3 promo code.

| | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| C1 | T | T | T | T | F | F | F | F |
| C2 | T | T | F | F | T | T | F | F |
| C3 | T | F | T | F | T | F | T | F |
| Waive fee | X | X | X | X | X | | X | |

Collapsed: existing customer waives regardless (R1-R4 -> `T - -`); new customer with promo waives (R5, R7 -> `F - T`); new customer without promo pays (R6, R8 -> `F - F`). 8 columns -> 3 rules.

## Coverage
Decision table coverage = columns exercised / feasible columns (of the collapsed table if collapsed).

## Gotchas
- Collapsing assumes the implementation really ignores the don't-care condition; for high risk, test one or two expanded columns too (implementation may differ from spec).
- Conditions that are not independent (age < 18 and age > 65 both true) create infeasible columns: remove, do not test.

## Verify
Every collapsed rule has one test, and the collapsed table was reviewed by the business owner.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 4.2.3 (full table, removing infeasible columns, merging columns where a condition does not affect the outcome, coverage as exercised over feasible columns, exponential growth of rules).
Removed: the unfetched Advanced Test Analyst source.
Method: documentation only; no commands were run.
