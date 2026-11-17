---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.k-omega-sst-model
name: k-omega-sst-model
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, turbulence-models, turbulence-modelling, k-omega-sst, menter, rans, shear-stress-transport, production-limiter, aerodynamics]
level: practitioner
status: gated
description: "Use Menter k-omega SST for adverse-pressure-gradient and separating aerodynamic flows, with correct inlet turbulence, mesh and production-limiter choices."
sources:
  - "Menter, Two-equation eddy-viscosity turbulence models for engineering applications (AIAA Journal 1994)"
  - "Menter, Kuntz and Langtry, Ten years of industrial experience with the SST turbulence model"
  - "NASA Langley Turbulence Modeling Resource"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# k-omega SST model

**Goal:** choose and configure SST for flows with adverse pressure gradients.

## Characteristics
- Blends k-omega near walls with k-epsilon in the freestream through blending functions, and limits eddy viscosity using the shear-stress transport relation (standard SST per NASA TMR: `nu_t = a1 k / max(a1 omega, Omega F2)` with `Omega` the vorticity magnitude and `a1 = 0.31`; SST-2003 uses the strain invariant `S` instead of `Omega`), which improves predictions under adverse pressure gradients.
- Needs `y+` about 1 for wall-resolved use; many codes apply automatic wall treatment that tolerates larger `y+`.
- Common in turbomachinery, high-lift and general RANS work.

## Settings
- Inlet/farfield (NASA TMR, external flow): omega between U/L and 10 U/L (L = approximate domain length), k between 1e-5 U^2/Re_L and 0.1 U^2/Re_L, giving freestream turbulent viscosity 1e-5 to 1e-2 times laminar. TMR calls these open to interpretation; SST-sust fixes omega = 5U/L and k = 1e-6 U^2 (Tu about 0.08%). Too high a freestream turbulence changes transition and skin friction.
- Production limiter: k production is limited to min(P, 20 beta* rho omega k) in standard SST (10 in SST-2003, applied to both equations); TMR recommends using it. Variants SST-V (vorticity-based production, often used for hypersonic bow shocks), SSTm, SSTs, SSTe are listed in TMR.
- Curvature correction option for rotation and curved flows; use only when needed.

## Known issues
- Over-predicts eddy viscosity in some separated regions and tends to predict later separation than reality for some flows (gated: unconfirmed, source is paywalled or blocked).
- Not a transition model; combine with a transition model (for example the gamma-Re_theta variant) for laminar-turbulent transition.

## Verify
- [ ] Flat plate `Cf` matches the published result in the solver.
- [ ] Sensitivity to freestream turbulence is tested with at least two values.
