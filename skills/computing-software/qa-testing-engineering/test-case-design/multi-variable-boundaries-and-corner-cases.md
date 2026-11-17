---
id: computing-software.qa-testing-engineering.test-case-design.multi-variable-boundaries-and-corner-cases
name: multi-variable-boundaries-and-corner-cases
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [corner-cases, multi-variable-boundaries, boundary-value-analysis, domain-testing, combinatorial-testing]
level: practitioner
status: draft
description: "Test boundaries across multiple variables: corner cases where several inputs sit at limits, dependent boundaries, and choosing which corners matter."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boundaries across multiple variables (corner cases)

**Goal:** find failures that occur only when two or more variables are at their limits together.

## Independent vs dependent boundaries
- **Independent:** each variable's range is fixed (width 1-100, height 1-100). Corners are the combinations of extremes: (1,1), (1,100), (100,1), (100,100).
- **Dependent (linear) boundaries:** the limit of one depends on another (width + height <= 150; loan amount <= 5 x income). The boundary is a line or surface; test on/off points along it (domain testing).

## Selecting corners
1. List the variables that participate in the same computation or constraint.
2. For independent ranges: take all 2^n extreme corners for small n; for larger n, all pairs of extremes (pairwise over {min, max}).
3. For dependent constraints: for each constraint, an ON point (exactly on the line), an OFF point (just outside), and an IN point (inside).
4. Add the corner of maximum resource use (largest file, most items, longest strings together) to catch overflow and timeouts.

## Example: parcel rule "length + girth <= 300 cm, each side <= 150 cm"
| Test | L | W | H | Note |
|---|---|---|---|---|
| 1 | 150 | 37.5 | 37.5 | L at max, combined = 300 (ON) |
| 2 | 150 | 37.5 | 37.6 | combined just over (OFF) |
| 3 | 151 | 10 | 10 | single side over |
| 4 | 1 | 1 | 1 | all minimum |

## Gotchas
- Rounding interacts with corners: combined measures computed in floats can land either side of the line.
- Corners at maximum size often expose performance problems rather than logic errors; record timing too.
- Corner explosion: prioritise corners tied to real-world risk (largest order, oldest account with most history).

## Verify
Each multi-variable constraint lists its ON/OFF points and the selected corners, with a reason for any corner omitted.
