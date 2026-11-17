---
id: computing-software.qa-testing-engineering.test-case-design.two-and-three-value-bva
name: two-and-three-value-bva
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [two-value-bva, three-value-bva, boundary-value-analysis, bva, black-box-testing, istqb]
level: practitioner
status: docs-checked
description: "Choose between 2-value and 3-value boundary value analysis, derive the values correctly for closed and open boundaries, and compute boundary coverage."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 2-value vs 3-value boundary value analysis

**Goal:** apply BVA as defined in ISTQB CTFL v4.0 4.2.2, with the right number of values per boundary.

## Definitions
Ordered partitions, each with a min and max boundary value.
- **2-value BVA**: for each boundary, the boundary value and its closest neighbour in the *adjacent* partition.
- **3-value BVA**: the boundary value and *both* neighbours (one on each side).

## Example: valid age 18-65 (integers)
| Method | Values for lower boundary | Upper boundary |
|---|---|---|
| 2-value | 17, 18 | 65, 66 |
| 3-value | 17, 18, 19 | 64, 65, 66 |

## Why 3-value
It catches defects 2-value misses. If the code says `age == 18` instead of `age >= 18`, 2-value (17, 18) passes; 3-value adds 19, which wrongly fails.
Use 3-value where the cost of a missed defect is high; this is practitioner judgement, not a syllabus rule.

## Coverage
Boundary coverage = boundary values exercised / boundary values identified (according to the chosen method).

## Gotchas
- Identify the boundaries from the spec *and* question them: "up to 65" inclusive or exclusive? Write it down.
- Partitions must be ordered for BVA; for unordered sets (colours) use EP only.
- Every boundary of every ordered partition, including the invalid ones (lowest/highest representable value).

## Verify
A table of boundaries with the derived values per method, and each value linked to a test with an explicit expected result.

## Checked
Date 2026-11-01. Documentation release: ISTQB CTFL Syllabus v4.0.1, section 4.2.2 (downloaded PDF).
Confirmed: section number, BVA only for ordered partitions, 2-value and 3-value coverage items, 3-value catching defects 2-value misses. Reworded the high-risk advice as judgement.
Method: documentation only; no commands were run.
