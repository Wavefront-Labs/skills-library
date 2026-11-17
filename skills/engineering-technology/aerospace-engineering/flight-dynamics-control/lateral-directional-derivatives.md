---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.lateral-directional-derivatives
name: lateral-directional-derivatives
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [lateral-derivatives, directional-stability, dihedral-effect, roll-damping, cn-beta, stability-derivatives]
level: practitioner
status: draft
description: "Estimate lateral-directional derivatives (Cy_beta, Cl_beta, Cn_beta, Cl_p, Cn_r) from geometry and relate them to dutch roll, roll and spiral modes."
sources:
  - "Nelson, Flight Stability and Automatic Control"
  - "Etkin and Reid, Dynamics of Flight"
  - "USAF DATCOM"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Lateral-directional derivatives

**Goal:** the lateral derivatives for roll, spiral and dutch-roll analysis.

## Key derivatives
- `Cn_beta` (weathercock): fin gives `Cn_beta_v = eta_v * V_V * CL_alpha_v * (1 + d_sigma/d_beta)`; the fuselage is usually destabilising. `Cn_beta > 0` is required.
- `Cl_beta` (dihedral effect): negative is stable. Contributions: geometric dihedral, wing sweep (negative increment), high wing (negative increment), fin.
- `Cy_beta`: negative, mostly fin and fuselage.
- Roll damping `Cl_p`: negative; wing dominated, roughly proportional to `CL_alpha` and aspect ratio effects.
- Yaw damping `Cn_r`: negative; fin dominated.
- Cross terms `Cl_r` (positive in normal flight) and `Cn_p` (often small).

## Mode relationships
- Dutch roll: frequency set by `Cn_beta` and yaw inertia; damping by `Cn_r` and `Cl_beta` coupling.
- Roll mode: time constant `~ -Ix / (q S b^2 Cl_p/(2V))`.
- Spiral: stable if `Cl_beta * Cn_r > Cl_r * Cn_beta` (a commonly used simplified condition).

## Procedure
1. Compute each derivative by component (wing, fuselage, fin), with DATCOM-type methods.
2. Assemble the dimensional A matrix for the states `[beta, p, r, phi]` (see six-dof-equations-of-motion-blocks).
3. Solve eigenvalues and compare with handling-qualities limits (see cooper-harper-handling-ratings).

## Gotchas
- Sign convention differences between wind and body axes cause mismatches in `Cl_beta` and `Cn_p`.
- Fuselage-wing interference changes `Cn_beta` strongly at high angles of attack.

## Verify
- [ ] The modal characteristics from the assembled matrix are physically plausible (dutch roll damped, spiral slowly stable or unstable).
