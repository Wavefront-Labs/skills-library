---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.anti-roll-bar-sizing
name: anti-roll-bar-sizing
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [anti-roll-bar, sway-bar, stabiliser-bar, roll-stiffness, torsion-bar, arb]
level: practitioner
status: gated
description: "Size an anti-roll bar from the roll stiffness target using torsion formulas, motion ratio and lever geometry, and check bar and bush stress."
sources:
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Anti-roll bar sizing

1. Target: roll stiffness contribution of the bar `K_bar` (N m/rad) from the total roll stiffness and LLTD plan.
2. Springs' roll stiffness at an axle: `K_spring = 0.5*k_wheel*t^2` (k_wheel wheel rate N/m, t track, m).
3. Bar torsional stiffness (straight section) `k_tors = G*J/L`, with `J = pi*d^4/32` (solid), G about 79 GPa for steel (gated: unconfirmed, source is paywalled or blocked); hollow: `J = pi*(do^4 - di^4)/32`.
4. Approximate roll stiffness of the bar: `K_bar = k_tors*t^2/a^2` with lever (arm) length a, ignoring arm bending and linkage ratio; multiply by the square of the link motion ratio. Arms and bushings reduce stiffness: correct with test or FE.
5. Stress: `tau = 16*T/(pi*d^3)` for solid; check at full-bump/roll against allowable (fatigue-limited, take supplier's design stress).
6. Because K scales with d^4, a 5% diameter change gives about 22% stiffness change (1.05^4 = 1.2155, computed).

**Gotchas:** bar is also effective in single-wheel bump (ride harshness); use disconnect or softer bush if needed.

## Verify
- [ ] Bar rate confirmed by a rig measurement vs prediction.
- [ ] Roll gradient and LLTD recalculated with the new bar.
