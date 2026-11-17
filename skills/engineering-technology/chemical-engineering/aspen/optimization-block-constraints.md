---
id: engineering-technology.chemical-engineering.aspen.optimization-block-constraints
name: optimization-block-constraints
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-sensitivity-and-optimisation, optimization-block-constraints, optimization-block, objective-function, constraints]
level: practitioner
status: gated
description: "Set up an Aspen Plus Optimization block with an objective, manipulated variables and constraints, and troubleshoot infeasible or noisy solves."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optimization block constraints

**Goal:** Set up an Aspen Plus Optimization block with an objective, manipulated variables and constraints, and troubleshoot infeasible or noisy solves.

## Steps
1. Define the objective in a Fortran expression using Define variables (for example profit = revenue - utility cost - raw material cost).
2. Declare the manipulated (Vary) variables with realistic lower and upper bounds, and add Constraints (purity, temperature limits, flooding) with their variable definitions.
3. Start from a feasible converged flowsheet; choose the algorithm per the help (SQP is the usual choice; confirm availability (gated: unconfirmed, source is paywalled or blocked)).
4. Tighten tolerances only after a coarse solution; check each constraint is active or slack as expected.
5. Do not combine an Optimization block with many nested design specs inside the loop; prefer EO mode for larger problems.

## Gotchas
- Noisy results (loose inner tolerances) mislead the optimiser.
- Check the optimum against a Sensitivity scan to avoid a local solution.

## Verify
- [ ] Constraints are satisfied at the solution.
- [ ] The optimum is stable to a different starting point.
