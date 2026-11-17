---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.airfoil-2d-cfd-workflow
name: airfoil-2d-cfd-workflow
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, aero-cfd, external-aerodynamics, airfoil-cfd, c-grid, alpha-sweep, naca-0012, airfoil-polar]
level: practitioner
status: draft
description: "Run a 2D airfoil RANS study: domain size, mesh, boundary conditions, turbulence model, alpha sweep, and comparison with published section data."
sources:
  - "NASA Langley Turbulence Modeling Resource (NACA 0012 case)"
  - "Abbott and von Doenhoff, Theory of Wing Sections"
  - "Solver user guides"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# 2D airfoil CFD workflow

**Goal:** a lift/drag/moment polar you can compare with test data.

## Setup
1. **Geometry:** closed trailing edge or small blunt edge; unit chord.
2. **Domain:** C- or O-mesh with the farfield at least 50 chords for subsonic cases (more for lifting flows if using a plain freestream boundary; a point-vortex far-field correction allows a smaller domain).
3. **Mesh:** wall `y+` about 1, 20-40 layers with growth 1.1-1.2, about 200-400 points around the airfoil, clustering at leading and trailing edges; check grid convergence.
4. **Solver:** compressible pressure far-field for transonic, incompressible for low speed; second-order upwind; steady RANS with SA or SST (add a transition model where laminar runs matter).
5. **Boundary conditions:** angle of attack set by rotating the freestream vector, not the mesh; freestream turbulence intensity documented.
6. **Sweep:** alpha from negative to stall in steps of 1-2 degrees, restarting each case from the previous solution; refine steps near stall.

## Post-processing
- `Cl`, `Cd`, `Cm` about the quarter chord, `Cp` distribution; compare with tests at matching Re and Mach.
- Check the wake for a sensible profile.

## Gotchas
- `Cl_max` and stall are not reliably predicted by steady RANS.
- Far-field too close gives biased lift at high alpha.

## Verify
- [ ] Mesh convergence at one alpha shows `Cl` and `Cd` change below tolerance.
- [ ] Lift slope and `Cd_min` are within expected scatter of test data.
