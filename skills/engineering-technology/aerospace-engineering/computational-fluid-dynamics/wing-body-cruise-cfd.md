---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.wing-body-cruise-cfd
name: wing-body-cruise-cfd
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, aero-cfd, external-aerodynamics, wing-body-cfd, transonic-cfd, fixed-cl, aeroelastic-shape, drag-counts]
level: advanced
status: draft
description: "Plan a wing-body cruise CFD study: geometry, aeroelastic shape, mesh strategy, trim, and how to compare with drag-workshop style data."
sources:
  - "AIAA Drag Prediction Workshop reports (DLR-F6 and NASA Common Research Model cases)"
  - "Slotnick et al., CFD Vision 2030 Study"
  - "Solver user guides"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Wing-body cruise CFD

**Goal:** drag and moment at transonic cruise suitable for configuration trades.

## Setup
1. **Geometry:** clean CAD, with the jig vs flight shape decided: flight-shape wing includes aeroelastic twist; comparing with test requires the measured deformed shape.
2. **Mesh:** structured or unstructured; boundary layer `y+` about 1, 30+ layers; refinement for the shock, wing-body junction, trailing edge and wake; for confidence use a grid family (medium, fine, extra fine) with refinement ratio about 1.5.
3. **Conditions:** cruise Mach and Reynolds number; run at fixed `CL` (let alpha float) for drag comparisons (many codes support a target-CL mode) or sweep alpha.
4. **Model:** RANS with SA (with QCR where available) or SST; a stated freestream turbulence level.
5. **Outputs:** pressure and viscous drag split, `CD` vs `CL`, `Cm` and spanwise loading; pressure coefficient cuts at stations.

## Analysis
- Report drag in counts (1 count = 0.0001); workshop-style variation between codes and models is often tens of counts at coarse levels and narrows with refinement.
- Compare to tunnel data with the same wall interference and aeroelastic corrections.

## Gotchas
- A grid that is fine on one wing may under-resolve the junction separation; check sensitivity.
- Trim drag needs the tail and the correct centre-of-gravity.

## Verify
- [ ] Drag vs grid-size plot shows convergence trend.
- [ ] CL target and Mach are fixed and recorded for every run.
