---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.high-lift-configuration-cfd
name: high-lift-configuration-cfd
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, aero-cfd, external-aerodynamics, high-lift-cfd, slat-flap, hilift-workshop, trap-wing, clmax-prediction]
level: advanced
status: draft
description: "Plan CFD of slat-flap configurations: meshing the gaps, transition, turbulence model sensitivity, and realistic expectations near CLmax."
sources:
  - "AIAA High Lift Prediction Workshop reports (NASA Trap Wing and other configurations)"
  - "Rumsey and Ying, Prediction of high lift: review of present CFD capability (Progress in Aerospace Sciences, 2002)"
  - "Slotnick et al., CFD Vision 2030"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# High-lift configuration CFD

**Goal:** loads and flow features of slats and flaps in take-off and landing settings.

## Meshing
- Resolve gaps and overlaps with 15-30 cells across each gap and boundary layer layers on every element; wakes of upstream elements must pass through well-resolved mesh over their entire path.
- Include brackets, tracks and fairings if the quantity of interest is sensitive to them; clean-wing results can differ strongly from the real configuration.

## Physics
- Laminar and transitional regions exist on slats and flap leading edges at low Re; specify transition locations (or use a transition model) to avoid unrealistic fully turbulent results.
- Merging wakes and confluent boundary layers challenge RANS models: compare SA with SST and a Reynolds-stress model.

## Expectations
- Linear-range lift and moment are usually predicted well; `CLmax` and stall onset are uncertain.
- Use workshop results (HiLiftPW series) to calibrate expectations for your method; participant scatter near stall has been substantial.

## Gotchas
- Wind-tunnel corrections and model support affect the validation data significantly.
- Mesh convergence needs refinement of gaps, not only global refinement.

## Verify
- [ ] Gap cell counts and layer counts are documented.
- [ ] Predicted `CL`-alpha slope matches data in the linear range before analysing stall.
