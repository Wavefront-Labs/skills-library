---
id: computing-software.qa-testing-engineering.test-case-design.measuring-equivalence-partition-coverage
name: measuring-equivalence-partition-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [ep-coverage, equivalence-partitioning, test-coverage, each-choice, istqb]
level: practitioner
status: docs-checked
description: "Measure equivalence partition coverage correctly: count items, handle multiple parameters with each-choice, and report coverage with untested partitions listed."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring equivalence partition coverage

**Goal:** state EP coverage as a defensible number. CTFL v4.0 4.2.1.

## Definition
EP coverage = partitions exercised by at least one test / total partitions identified, as a percentage. Valid and invalid partitions both count.

## Single parameter
Partitions P1-P6, tests hit P1, P3, P4, P6 -> 4/6 = 67%. Report P2 and P5 as untested with a reason or a plan.

## Multiple parameters
- **Each-choice coverage** (minimum): every partition of every parameter appears in at least one test. Valid partitions can be combined in one test; each **invalid** partition gets its own test with all other parameters valid.
- Tests needed for each-choice of valid partitions = max number of valid partitions of any single parameter.
- Each Choice coverage does not take combinations of partitions into account; combinations beyond that are combinatorial testing, not EP coverage.

### Example
Size {S, M, L} valid + {blank} invalid; Colour {red, blue} valid + {unknown} invalid.
| Test | Size | Colour |
|---|---|---|
| 1 | S | red |
| 2 | M | blue |
| 3 | L | red |
| 4 | blank | red |
| 5 | M | unknown |
7/7 partitions -> 100% EP coverage with 5 tests.

## Measuring in automation
Tag parametrized cases with partition IDs (`pytest.param(..., id="P3-too-short")`) and compute coverage from the test report against the partition table.

## Gotchas
- 100% EP coverage says nothing about boundaries; combine with BVA.
- Coverage is only as good as the partition analysis; missed partitions do not appear in the denominator.
- Do not count the same test twice for two invalid partitions in one case: it covers neither reliably.

## Verify
Coverage report lists partition IDs with linked tests and explicitly names uncovered partitions.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL v4.0.1 syllabus (section 4.2.1): coverage items are the partitions including invalid ones, coverage is partitions exercised by at least one test divided by identified partitions as a percentage, and Each Choice coverage requires every partition of every set at least once and ignores combinations. The one-invalid-partition-per-test advice is common practice, not syllabus text. Removed: nothing else.
Method: documentation only; no commands were run.
