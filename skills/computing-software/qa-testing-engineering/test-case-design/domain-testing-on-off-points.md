---
id: computing-software.qa-testing-engineering.test-case-design.domain-testing-on-off-points
name: domain-testing-on-off-points
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [domain-testing, on-off-points, boundary-value-analysis, domain-analysis, linear-boundaries, istqb-ta]
level: practitioner
status: gated
description: "Apply domain testing: on, off, in and out points for boundaries, including multi-variable linear boundaries like x + y <= 100 that simple BVA misses."
sources:
  - https://www.oreilly.com/library/view/the-domain-testing/9780989811903/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain testing: on, off, in and out points

**Goal:** test boundaries precisely, including boundaries defined by several variables. Kaner, Padmanabhan & Hoffman, *The Domain Testing Workbook* (gated: unconfirmed, source is paywalled or blocked).

## Points for each boundary
- **On point**: on the boundary itself.
- **Off point**: as close as possible to the boundary, on the other side from the on point (for a closed boundary `x <= 100`, on = 100 (in domain), off = 101 (out)). For an open boundary `x < 100`, on = 100 (out of domain), off = 99 (in).
- **In point**: a typical value inside the domain. **Out point**: a typical value outside.
Precision decides "as close as possible": 100.01 for money with cents, 101 for integers.

## Multi-variable (linear) boundaries
Rule: approve if `debt + new_loan <= 0.4 * income`.
- On point: values where `debt + new_loan == 0.4 * income` exactly (income 100000, debt 30000, loan 10000).
- Off point: just over (loan 10000.01).
- Test several on points along the boundary line (different income levels), because a defect may tilt or shift the line (e.g. code uses `0.4 * net_income`).

## Defects domain testing targets
Wrong operator (`<` vs `<=`), shifted boundary (`<= 99`), tilted boundary (wrong coefficient), missing boundary, extra boundary.

## Gotchas
- Choosing off points too far away (95 instead of 99) misses off-by-one defects.
- Floating-point boundaries need the representation's precision (`floating-point-and-currency-boundaries`).

## Verify
For each boundary, the test set has an on point and an off point, and for linear boundaries at least two on points along the line.

## Checked

2026-10-28. Confirmed: Nothing source-specific; the O'Reilly page is blocked (403). Gated: the book attribution (Kaner, Padmanabhan & Hoffman). On/off-point rules are worked definitions. Removed: Syllabus section number and the erroring ISTQB source.

Method: documentation only; no commands were run.
