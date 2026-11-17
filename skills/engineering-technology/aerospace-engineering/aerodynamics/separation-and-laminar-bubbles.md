---
id: engineering-technology.aerospace-engineering.aerodynamics.separation-and-laminar-bubbles
name: separation-and-laminar-bubbles
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, boundary-layer, viscous-flow, flow-separation, laminar-separation-bubble, trip-strip, turbulator, adverse-pressure-gradient]
level: advanced
status: draft
description: "Diagnose boundary-layer separation and laminar separation bubbles from pressure distributions, and choose fixes such as trips, shape changes or turbulators."
sources:
  - "Schlichting and Gersten, Boundary-Layer Theory"
  - "Mueller, Low Reynolds number vehicles (AGARDograph 288)"
  - "Gad-el-Hak, Flow Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Separation and laminar separation bubbles

**Goal:** identify and mitigate separated flow in 2D and 3D wings.

## Mechanism
- Adverse pressure gradient decelerates near-wall flow; when wall shear reaches zero, flow separates.
- Laminar flow separates easily. At low Reynolds numbers (roughly below 5e5) a laminar separation bubble forms, transitions in the shear layer, and may reattach as a turbulent layer. Short bubbles increase drag modestly; long bubbles or bursting bubbles produce abrupt lift loss.

## Recognising them
- Pressure distribution: a flat region (plateau) followed by a sharp pressure recovery.
- CFD: skin-friction coefficient crossing zero and returning positive.
- Test: oil flow, tufts, or thermography.

## Fixes
1. Turbulators: trip strips or zig-zag tape ahead of the predicted separation; tape thickness must be at or below the local boundary-layer thickness to limit drag.
2. Section redesign: concave pressure recovery shaping (Stratford-type) to keep the layer attached.
3. Vortex generators or suction on larger surfaces.
4. Higher Reynolds number through chord or speed.

## Gotchas
- Trips add parasite drag; apply only where polars show a bubble penalty.
- RANS without transition modelling misses bubbles; use a transition model and unsteady checks.

## Verify
- [ ] The separation point from CFD agrees with oil-flow or tuft observation.
- [ ] After the fix, skin friction no longer crosses zero in the design range.
