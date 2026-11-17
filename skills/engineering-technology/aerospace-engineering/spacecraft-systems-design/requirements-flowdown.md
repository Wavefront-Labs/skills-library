---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.requirements-flowdown
name: requirements-flowdown
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [requirements-flowdown, requirements-allocation, traceability, verification-matrix, mission-systems-engineering, nasa-systems-engineering]
level: practitioner
status: docs-checked
description: "Flow mission requirements down to subsystems with allocation, margins, traceability and a verification method for each requirement."
sources:
  - https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/
  - https://www.nasa.gov/reference/4-2-technical-requirements-definition/
  - https://www.nasa.gov/reference/6-2-requirements-management/
  - https://www.nasa.gov/reference/5-3-product-verification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Requirements flow-down

**Goal:** every lower-level requirement traces to a parent, and every parent is satisfied by children.

## Levels
Stakeholder expectations, customer requirements, technical product requirements, product component requirements, and the interfaces between them (NASA SE Handbook wording).

## Procedure
1. Capture stakeholder expectations and write measurable mission requirements (for example pointing accuracy, data volume per day, design life, orbit).
2. Derive technical requirements by analysis (budgets, error trees); keep the rationale for each, not just the number. If a requirement states a method of implementation, record why the design was limited to it.
3. Allocate to subsystems with margin: mass, power, data rate, pointing error, reliability. Track key performance margins and assess every change against them (see mass-and-power-margin-philosophy).
4. Write each requirement as a "shall" statement with a measurable value, and an assumed verification method.
5. Keep parent-child links in a traceability tool or database with bidirectional traceability: any requirement traces to its parent and to its allocated children.
6. Verification method for each: test, analysis, inspection, or demonstration; record results in a requirements compliance or verification matrix and plan the verification events (see environmental tests).
7. Manage changes through configuration control with the requirements baseline, and review open items at each design review milestone (see design-review-milestones).

## Gotchas
- Requirements that name a solution rather than a need lock the design early.
- Allocation without margins forces late re-allocation; changes that cannot fit the established resource margins should most likely be denied.
- Changes must be propagated downward and upward through the traceability links.

## Verify
- [ ] Every requirement has a parent (or is a top-level expectation), allocated children where decomposed, a verification method and an owner.

## Checked
2026-11-01. Confirmed against NASA Systems Engineering Handbook online sections 4.2 (shall statements, rationale for implementation-limiting requirements), 6.2 (bidirectional traceability, performance margins, change assessment against resource margins) and 5.3 (test, analysis, inspection, demonstration; verification matrix). Removed: TBD/TBR handling, the singular/unambiguous wording rule, interface control document step, and the Wertz-Larson and Fortescue book sources.
Method: documentation only; no commands were run.
