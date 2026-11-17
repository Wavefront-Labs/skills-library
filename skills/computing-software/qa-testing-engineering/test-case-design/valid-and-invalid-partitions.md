---
id: computing-software.qa-testing-engineering.test-case-design.valid-and-invalid-partitions
name: valid-and-invalid-partitions
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [equivalence-partitioning, invalid-partitions, each-choice-coverage, black-box-testing, negative-testing, istqb]
level: practitioner
status: docs-checked
description: "Apply equivalence partitioning with valid and invalid partitions: one invalid partition per test to avoid defect masking, and each-choice coverage across parameters."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Valid and invalid partitions

**Goal:** minimum tests that exercise every partition, without one error hiding another. ISTQB CTFL v4.0 4.2.1.

## Procedure
1. For each input, split its domain into partitions the system should treat the same way. Example, age field for an insurance quote (allowed 18-75):
   - valid: 18-75
   - invalid: < 18, > 75, non-numeric, empty, decimal (if integers only)
2. **Valid partitions can be combined** in one test (all inputs valid).
3. **Invalid partitions are tested one per test**, with all other inputs valid. Otherwise the first validation error masks the others: a form with invalid age *and* invalid postcode may only report age, so the postcode check is never exercised.
4. Coverage = partitions exercised / total partitions.

## Each-choice coverage (multiple parameters)
Each partition of each parameter appears in at least one test. Number of tests = max partitions of any single parameter (for valid ones), plus one per invalid partition.

| Test | Age | Country | Payment | Expected |
|---|---|---|---|---|
| 1 | 30 | UK | card | quote |
| 2 | 70 | DE | invoice | quote |
| 3 | 17 | UK | card | age error |
| 4 | 30 | XX | card | country error |
| 5 | 30 | UK | bitcoin | payment error |

## Gotchas
- Partitions come from the *specification and the implementation*: "UK and DE use different tax code paths" makes them different partitions even if the UI treats them alike. Ask developers.
- Invalid partitions are often under-specified; agree the expected error per partition.

## Verify
A table listing every partition per input with the test id covering it, and invalid partitions each in their own test.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 4.2.1 (partitions, valid and invalid partitions, coverage as partitions exercised over total, Each Choice coverage ignores combinations) and the v4.0 change log (invalid partitions tested in isolation to avoid defect masking).
Removed: the unfetched Advanced Test Analyst source.
Method: documentation only; no commands were run.
