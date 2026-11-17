---
id: engineering-technology.aerospace-engineering.aerodynamics.transition-prediction-methods
name: transition-prediction-methods
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, boundary-layer, viscous-flow, transition, transition-prediction, e-n-method, tollmien-schlichting, crossflow, michel-criterion]
level: advanced
status: draft
description: "Predict laminar-turbulent transition with e^N, Michel and similar methods, and list the mechanisms (TS, crossflow, bypass, roughness) that decide it."
sources:
  - "Schlichting and Gersten, Boundary-Layer Theory"
  - "Arnal, transition prediction lecture notes (AGARD/VKI)"
  - "Drela, XFOIL documentation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Transition prediction

**Goal:** locate transition for drag estimation and laminar-flow design.

## Mechanisms
- **Tollmien-Schlichting (TS) waves:** natural transition, low freestream turbulence.
- **Crossflow instability:** swept wings with favourable pressure gradient; dominant above sweep of roughly 20-25 degrees.
- **Bypass:** high freestream turbulence or large roughness skips the linear stage.
- **Attachment-line contamination:** at the leading edge of swept wings; controlled by leading-edge radius and Reynolds number.
- **Separation-induced:** laminar separation bubble reattaching turbulent.

## Methods
1. **Empirical (Michel):** transition when `Re_theta` exceeds a function of `Re_x`; cheap, uncalibrated for modern sections.
2. **e^N method:** compute amplification of TS (and crossflow) disturbances with linear stability theory along the boundary layer; transition at `N` = N_crit. N of about 9 matches average tunnel conditions and 11-14 low-turbulence or flight conditions; XFOIL uses Ncrit with this meaning.
3. **Correlation-based CFD models:** the gamma-Re_theta (transition SST) model and the SA-based variants fit into RANS; they need fine mesh and careful inlet turbulence settings.

## Practice
- Specify turbulence intensity and turbulent viscosity ratio at the inlet; transition location in CFD is strongly sensitive to these.
- Use a mesh with y+ about 1 and ~50-100 points streamwise on the laminar region.
- Compare predicted transition with flight or tunnel IR thermography or sublimating chemicals where available.

## Verify
- [ ] Predicted transition is bracketed by smooth-surface and trip-forced cases.
- [ ] N_crit or turbulence level assumed is stated and justified.
