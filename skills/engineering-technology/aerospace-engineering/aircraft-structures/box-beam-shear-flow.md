---
id: engineering-technology.aerospace-engineering.aircraft-structures.box-beam-shear-flow
name: box-beam-shear-flow
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, thin-walled, semi-monocoque, shear-flow, shear-centre, idealised-section, bredt-batho, multi-cell]
level: practitioner
status: draft
description: "Compute shear flow and shear centre in thin-walled open and closed sections for wing boxes, including idealised booms and multi-cell torsion."
sources:
  - "Megson, Aircraft Structures for Engineering Students"
  - "Bruhn, Analysis and Design of Flight Vehicle Structures"
  - "Niu, Airframe Structural Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Shear flow in box beams

**Goal:** shear flow distribution and twist for sizing webs and skins.

## Basics
- Open section: `q(s) = - (Vy/Ixx) integral(t y ds)` (symmetric bending case); for a section idealised with booms of area `B_r` at `y_r`: `q_change = - (Vy/Ixx) B_r y_r` across each boom.
- Closed single cell: `q = q_open + q_0`, with `q_0` found from moment equilibrium about a convenient point, or from zero twist if the load acts through the shear centre.
- Torque in a closed section: Bredt-Batho `T = 2 A q`; twist `dtheta/dz = (1/(2 A G)) oint (q/t) ds`.
- Multi-cell: all cells have the same twist rate; solve simultaneous equations for each cell's shear flow with torque equilibrium.
- Shear centre: point where a shear load causes no twist.

## Procedure
1. Compute section properties (neutral axis, `Ixx`, `Iyy`, `Ixy`) from booms and web effective areas (skin carries a fraction of bending load via effective width).
2. Determine shear load and its line of action from the wing loads.
3. Compute open-section shear flow, add closure shear flows.
4. Check web shear stress `q/t` against buckling and allowable (see panel buckling skill).

## Gotchas
- Sign conventions and direction of `s`.
- Neglecting skin buckling effects on effective area when skins buckle before limit load.

## Verify
- [ ] Vertical shear flow resultants equal the applied shear; torques about a point balance.
