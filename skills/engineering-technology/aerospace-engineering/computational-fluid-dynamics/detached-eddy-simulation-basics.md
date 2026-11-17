---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.detached-eddy-simulation-basics
name: detached-eddy-simulation-basics
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, turbulence-models, turbulence-modelling, detached-eddy-simulation, des, ddes, iddes, les, scale-resolving, hybrid-rans-les]
level: advanced
status: draft
description: "Plan hybrid RANS-LES (DES, DDES, IDDES) runs: where they apply, grid and time-step requirements, and common failures like grid-induced separation."
sources:
  - "Spalart et al., Comments on the feasibility of LES for wings and on a hybrid RANS/LES approach (1997)"
  - "Spalart et al., A new version of detached-eddy simulation, resistant to ambiguous grid densities (2006)"
  - "Sagaut, Large Eddy Simulation for Incompressible Flows"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Detached-eddy simulation (DES) basics

**Goal:** resolve large unsteady separated structures at affordable cost.

## Idea
RANS is used in the attached boundary layer; LES in separated regions. DES (Spalart 1997) switches the length scale in the SA model to `min(d, C_DES * Delta)`, where `Delta` is the local grid spacing. DDES (delayed) adds a shielding function to keep RANS in boundary layers when the grid is fine; IDDES allows wall-modelled LES in attached regions.

## Requirements
- Mesh: isotropic, LES-quality cells in the separated region (cell size resolving the energy-containing eddies), RANS-appropriate cells in the boundary layer. A sudden mesh transition invites errors.
- Time step: roughly CFL of about 1 in the LES region, using a temporal order of second order; sample for several flow-through times and discard transient.
- Numerics: low-dissipation (central or blended) schemes in the LES region.

## Failure modes
- Grid-induced separation: ambiguous grid in the boundary layer where DES switches early; DDES mitigates.
- Log-layer mismatch in wall-modelled LES.
- Cost: 10 to 100 times RANS or more.

## Practice
1. Do a RANS run first; use it to size the mesh and identify the separated region.
2. Use DDES or IDDES, not plain DES, in production.
3. Compare mean and RMS data with experiment where possible.

## Verify
- [ ] Ratio of resolved to modelled turbulent kinetic energy in the LES region is reported and above about 80%.
- [ ] Statistics converge with additional sampling time.
