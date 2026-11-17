---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.rans-failure-modes
name: rans-failure-modes
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, turbulence-models, turbulence-modelling, rans-limitations, corner-separation, massive-separation, eddy-viscosity, boussinesq, qcr]
level: advanced
status: draft
description: "List where steady RANS predictions fail (corner flows, massive separation, transition, rotating or curved flows) and what to do about each."
sources:
  - "Slotnick et al., CFD Vision 2030 Study (NASA CR-2014-218178)"
  - "Spalart, Strategies for turbulence modelling and simulations"
  - "AIAA Drag Prediction Workshop reports"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# RANS failure modes

**Goal:** know when a RANS answer should not be trusted and what to do next.

## Known weak areas
- **Corner and junction flows:** wing-body or wing-pylon junction separation is over-predicted by linear eddy-viscosity models; QCR (quadratic constitutive relation) or Reynolds-stress models help.
- **Massive separation and high-lift near CLmax:** steady RANS usually cannot predict CLmax accurately; scatter is large.
- **Transition:** fully turbulent assumption misses laminar run; add a transition model and a specified inflow turbulence.
- **Strong curvature, rotation, swirl:** curvature corrections or Reynolds stress models.
- **Unsteady shedding, buffet:** need URANS or hybrid methods (DES).
- **Shock-boundary-layer interaction:** model-dependent; compare multiple models.

## Practice
1. Declare the intended use: attached cruise forces (RANS is fit for use), separated (not).
2. Run at least two turbulence models, report the spread as a form of uncertainty.
3. Validate against a nearby test data set before extrapolating.
4. Escalate to hybrid RANS-LES, scale-resolving, or test when the quantity depends on separation.

## Gotchas
- A converged steady solution can hide an unsteady flow; monitor force oscillations.
- Spread between models is not the same as error, but a large spread is a warning.

## Verify
- [ ] Report states the use case, models used, and the fidelity limit.
