---
id: computing-software.qa-testing-engineering.test-case-design.robustness-and-worst-case-boundary-testing
name: robustness-and-worst-case-boundary-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [robustness-testing, worst-case-boundaries, boundary-value-analysis, black-box-testing, invalid-inputs]
level: practitioner
status: verified
description: "Extend BVA with robustness values (just outside valid range) and worst-case combinations (Cartesian product of boundary values) and size the test count."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Robustness and worst-case boundary testing

**Goal:** choose how far BVA goes beyond the basic single-fault values. Terminology from Jorgensen, *Software Testing: A Craftsman's Approach* (book not re-read; the 4n+1, 6n+1, 5^n, 7^n counts match course notes such as the York University EECS 4313 boundary-value module, and the n = 3 totals below were computed).

## Variants for n variables
| Variant | Values per variable | Combination rule | Tests |
|---|---|---|---|
| Normal BVA | min, min+, nom, max-, max | vary one at a time, others nominal | 4n + 1 |
| Robustness | adds min-, max+ (invalid) | one at a time | 6n + 1 |
| Worst-case | min, min+, nom, max-, max | Cartesian product | 5^n |
| Robust worst-case | 7 values | Cartesian product | 7^n |

For n = 3: normal 13, robust 19, worst-case 125, robust worst-case 343.

## When to use which
- **Normal BVA:** independent variables, single-fault assumption (most failures come from one variable at a boundary).
- **Robustness:** whenever invalid input must be handled gracefully: public APIs, user input, file parsers. Expected result is a defined error, not a crash or silent clamp.
- **Worst-case:** variables interact physically or numerically (e.g. dimensions x weight -> shipping band, interest = rate x term x amount), or safety-critical.
- Robust worst-case: rarely, small n, critical systems.

## Expected results for robustness values
Decide for each: reject with error, clamp to limit, or accept (when the spec was loose). Clamping silently is a common hidden defect; make it explicit.

## Implementing
```python
import itertools
W = [1, 2, 50, 99, 100]       # weight kg boundaries
L = [1, 2, 60, 119, 120]      # length cm
cases = list(itertools.product(W, L))   # 25 worst-case combinations (len checked = 25)
```
Feed into a parametrized test with an oracle function or a reference table for expected bands.

## Gotchas
- Worst-case explodes fast; use it only for interacting variables, and pairwise for the rest.
- Invalid values in combination: still one invalid per test to keep failures diagnosable.

## Verify
The test design states the variant chosen per variable group with a reason and the resulting test count.
