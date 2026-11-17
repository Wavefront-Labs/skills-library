---
id: engineering-technology.aerospace-engineering.aerodynamics.vortex-generators-passive-flow-control
name: vortex-generators-passive-flow-control
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, boundary-layer, viscous-flow, vortex-generators, flow-control, gurney-flap, passive-flow-control, separation-control]
level: practitioner
status: draft
description: "Size and place vortex generators and similar passive devices to delay separation, and weigh their drag cost on wings, nacelles and control surfaces."
sources:
  - "Lin, Review of research on low-profile vortex generators (Progress in Aerospace Sciences)"
  - "Gad-el-Hak, Flow Control"
  - "Raymer, Aircraft Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Vortex generators and passive flow control

**Goal:** add momentum to the boundary layer to delay separation without a large drag penalty.

## Practice
- Vane-type VGs are small fins at an angle of attack (commonly around 15-20 degrees) to the local flow, in counter-rotating or co-rotating pairs. Low-profile (sub-boundary-layer) VGs have heights of roughly 0.2-0.5 of the local boundary layer thickness and have lower drag than conventional ones.
- Placement: upstream of the separation point (about 10-30 boundary-layer thicknesses ahead is typical to let the vortices mix), spaced a few device heights apart.
- Typical uses: wing upper surfaces near the flap or aileron to maintain control authority, nacelle strakes, aft fuselage upsweep, wind-turbine blade retrofits.
- Gurney flaps: a small tab at the trailing edge, a percent or two of chord, raise `cl` at a drag cost and are used in racing and some UAVs.

## Procedure
1. Locate separation from CFD or tufts.
2. Choose VG type, height, angle, spacing from the cited literature, then refine with CFD (include device-resolved or source-term models).
3. Test or compute the drag change at cruise; check that clean-wing stall behaviour is not worsened.

## Gotchas
- VGs can improve low-speed performance but cost drag at cruise: remove or limit them to critical regions.
- Placement downstream of separation does nothing.
- Retrofit on certified aircraft requires a design change approval.

## Verify
- [ ] Separation reduces or disappears in the CFD or tuft test with VGs.
- [ ] Cruise drag penalty is quantified.
