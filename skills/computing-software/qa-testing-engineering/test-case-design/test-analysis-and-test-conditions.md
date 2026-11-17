---
id: computing-software.qa-testing-engineering.test-case-design.test-analysis-and-test-conditions
name: test-analysis-and-test-conditions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-analysis, test-conditions, test-basis, test-process, istqb, testability, coverage-items]
level: practitioner
status: draft
description: "Analyse the test basis into prioritised test conditions: what to test, defects found in the basis itself, and coverage items each technique will derive tests from."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test analysis: from test basis to test conditions

**Goal:** answer "what to test" before "how". ISTQB CTFL v4.0 1.4.1, CTAL-TA v4.0 1.2.

## Procedure
1. **Collect the test basis**: requirements, user stories + acceptance criteria, designs, API specs, risk analysis, existing system behaviour. Record versions.
2. **Evaluate it for defects** while reading: ambiguity ("fast", "user-friendly"), contradictions, missing error cases, untestable statements. Raise these as review comments now; it is the cheapest defect removal you will do.
3. **Identify features and sub-features**, then for each, **test conditions**: a testable aspect, e.g. "discount applied when basket > 100", "discount not applied to gift cards", "login locks after 5 failures".
4. **Prioritise conditions** by risk (likelihood x impact).
5. **Choose the technique** per condition, which defines the coverage items: partitions (EP), boundary values (BVA), rules (decision table), transitions (state model).
6. **Record traceability** basis item -> condition -> test case.

## Level of detail
- Low-detail conditions ("checkout discounts") suit experienced testers and fast-moving basis; high-detail suits regulated work and junior testers. Pick on purpose.

## Gotchas
- Writing test cases before conditions produces lots of tests for easy areas and none for the hard ones.
- Acceptance criteria are not the full set of conditions; add negative and non-functional conditions.

## Verify
Every high-risk requirement has at least one condition; every condition traces to a basis item or a stated risk.
