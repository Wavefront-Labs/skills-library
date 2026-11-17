---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.first-cell-height-from-y-plus
name: first-cell-height-from-y-plus
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, meshing, mesh-generation, y-plus, first-cell-height, wall-functions, boundary-layer-mesh, skin-friction]
level: practitioner
status: gated
description: "Compute the wall-adjacent cell height for a target y+ from Reynolds number and a skin-friction estimate, and check the achieved y+ after the run."
sources:
  - "Schlichting and Gersten, Boundary-Layer Theory"
  - "White, Viscous Fluid Flow"
  - "Solver user guides on wall treatment"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# First cell height from y+

**Goal:** place the first cell centre at a chosen `y+`.

## Estimate
`y+ = y u_tau / nu`, `u_tau = U sqrt(Cf/2)`. With a flat-plate turbulent estimate `Cf = 0.026 Re_x^(-1/7)` (Schlichting-type correlation (gated: unconfirmed, source is paywalled or blocked)):
`y = y+ * L * Re_L^(-13/14) / sqrt(0.013)`, about `8.77 * y+ * L * Re_L^(-13/14)` (algebra recomputed).
Worked example: chord 1 m, `Re = 6e6`, target `y+ = 1`: `y ~ 4.5e-6 m` (recomputed 4.46e-6). This y is the wall distance at which y+ is evaluated, normally the first cell centre, so the first cell height is about twice this.

## Targets
- Wall-resolved (low-Re) models such as k-omega SST, Spalart-Allmaras: `y+` of about 1 (up to roughly 5 is often tolerated).
- Wall functions: `y+` of about 30-300 (gated: unconfirmed, source is paywalled or blocked), avoiding the buffer layer 5-30.
- Transition models: y+ of about 1 and fine streamwise spacing.

## Procedure
1. Estimate at the cruise `Re` for the longest chord; use the highest `Cf` location (leading edge region and shocks give higher local values).
2. Build the mesh, run the solution, plot `y+` on the wall; adjust the first cell height and rerun.
3. Report maximum and average `y+`.

## Gotchas
- Flat-plate estimates under-predict `y+` near leading edges and shock feet; check after the run.
- Compressible flows: use the wall density and viscosity in the definition.

## Verify
- [ ] Post-processed y+ map is within the target range over more than about 95% of the wall.
