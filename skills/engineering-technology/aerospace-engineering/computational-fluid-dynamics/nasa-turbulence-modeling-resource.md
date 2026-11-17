---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.nasa-turbulence-modeling-resource
name: nasa-turbulence-modeling-resource
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, verification-validation, cfd-uncertainty, turbulence-modeling-resource, tmr, code-verification, flat-plate, bump-in-channel, grid-families]
level: practitioner
status: draft
description: "Use the NASA Langley Turbulence Modeling Resource verification cases (flat plate, bump, airfoil) to check that your solver implements a turbulence model correctly."
sources:
  - "NASA Langley Research Center Turbulence Modeling Resource (turbulence model descriptions, grids and reference results)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# NASA Turbulence Modeling Resource (TMR)

**Goal:** verify that a solver's turbulence model matches a reference implementation.

## What it provides
Descriptions of standard models (SA variants, SST variants and others), grid families, and reference results from established codes (for example CFL3D and FUN3D) for verification cases such as the 2D zero-pressure-gradient flat plate, the 2D bump-in-channel, a NACA 0012 airfoil and others.

## Procedure
1. Pick the model variant used in your solver and the TMR version matching it exactly (SA vs SA-noft2, SST vs SST-V).
2. Download the grid family and boundary-condition description; use the same boundary conditions and freestream values.
3. Run on the finest grids (and a refinement sequence), compare `Cf`, velocity profiles, forces and pressure to the reference values.
4. Quantify differences; apply a grid-convergence check to extrapolate.

## Practice
- Differences in model constants, limiters or wall treatment show up as differences in `Cf` profiles; trace them to the code's documentation.
- Keep the results with the solver's validation record for the project.

## Gotchas
- Using a variant different from the TMR reference is the most common reason for a mismatch.
- Solvers may use wall functions by default; set wall-resolved treatment for the verification cases.

## Verify
- [ ] `Cf` and velocity profile on the finest grid agree with reference results to well within the grid-convergence band.
