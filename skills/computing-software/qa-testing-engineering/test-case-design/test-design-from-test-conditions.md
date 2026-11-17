---
id: computing-software.qa-testing-engineering.test-case-design.test-design-from-test-conditions
name: test-design-from-test-conditions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-design-activity, test-process, test-cases, coverage-items, istqb]
level: practitioner
status: draft
description: "Run the test design activity: turn test conditions into coverage items and prioritised test cases with explicit inputs, expected results and traceability."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test design: from test conditions to test cases

**Goal:** answer "how to test" for each test condition analysis produced (CTFL v4.0 1.4.1). Analysis says *what*; design says *how*, at a level a tester or script can execute.

## Steps
1. Take the prioritised test conditions (e.g. "discount applied for gold members").
2. Pick a technique per condition from its nature: ranges -> EP/BVA, rule combinations -> decision table, lifecycle -> state transition, flows -> use case, interacting parameters -> pairwise, code risk -> branch coverage.
3. Derive **coverage items** from the technique (partitions, boundary values, rules, transitions, branches). This is what you count for coverage.
4. Build test cases: preconditions, inputs, expected result (from the oracle, never from running the system), postconditions, priority.
5. Identify the **test data** and **environment** each case needs; feed these to implementation.
6. Record traceability: condition -> coverage item -> test case.

## Test case template
| Field | Example |
|---|---|
| ID / title | TC-DISC-04 Gold member at 100.00 threshold |
| Covers | COND-12, BVA boundary 100.00 |
| Preconditions | Customer C-gold exists, cart empty |
| Steps / input | Add items totalling 100.00, checkout |
| Expected | 10% discount, total 90.00 |
| Priority | High (revenue rule) |

## Gotchas
- Logical (abstract) cases first, concrete values later; keeps the design reusable across data sets.
- One test case can cover several coverage items, but its failure must still point to one cause.
- Design is also where you find spec defects: an expected result you cannot state is a question for the product owner.
- Stop when the agreed coverage target per technique is reached, not when ideas run out.

## Verify
Every high-priority condition has at least one case; coverage per technique is computable (items covered / items identified); each case has a stated expected result.
