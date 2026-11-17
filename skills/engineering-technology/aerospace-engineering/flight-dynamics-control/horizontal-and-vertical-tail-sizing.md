---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.horizontal-and-vertical-tail-sizing
name: horizontal-and-vertical-tail-sizing
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [tail-sizing, tail-volume-coefficient, horizontal-tail, vertical-tail, stabiliser-sizing, static-stability]
level: practitioner
status: draft
description: "Size horizontal and vertical tails with tail volume coefficients, then verify with static margin, trim, rotation and engine-out yaw requirements."
sources:
  - "Raymer, Aircraft Design: A Conceptual Approach"
  - "Roskam, Airplane Design"
  - "Nelson, Flight Stability and Automatic Control"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tail volume sizing

**Goal:** first-pass tail areas, then checked against stability and control requirements.

## Tail volume coefficients
- Horizontal: `V_H = S_h * l_h / (S_w * c_bar)`.
- Vertical: `V_V = S_v * l_v / (S_w * b_w)`.
- `l` is the distance between the tail's aerodynamic centre and the wing's (or CG for some definitions; state which).
- Typical historical values (Raymer's table): general aviation single-engine about 0.7 (horizontal) and 0.04 (vertical); transport about 1.0 and 0.09; twin-engine light aircraft about 0.8 and 0.07. Use as starting values (gated: unconfirmed, source is paywalled or blocked).

## Procedure
1. Take `V_H` and `V_V` from similar aircraft; choose tail arm from the fuselage layout.
2. Compute `S_h` and `S_v`.
3. Verify:
   - Static stability: `Cm_alpha` includes tail contribution `-eta V_H CL_alpha_t (1 - d_eps/d_alpha)`; confirm the static margin target (see neutral-point-static-margin).
   - Trim and rotation: elevator authority at forward CG (see cg-envelope-limits).
   - Directional: `Cn_beta > 0` with enough margin; engine-out minimum control speed for multi-engine aircraft.
   - Spin recovery and, if relevant, deep-stall for T-tails.
4. Update areas, iterate with weight and drag.

## Gotchas
- Tail size is not set by volume coefficient alone; engine-out yaw and rotation commonly set the vertical and horizontal tail.
- T-tails sit outside the wing wake at cruise but may enter it at high angles of attack.
- Fuselage-mounted engines add yaw moments.

## Verify
- [ ] The final tail passes all the stability and control checks, not just the volume coefficient target.
