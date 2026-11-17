---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.static-stability-factor-and-rollover-risk
name: static-stability-factor-and-rollover-risk
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [static-stability-factor, ssf, rollover, rollover-threshold, track-width, cg-height]
level: practitioner
status: gated
description: "Compute the static stability factor and rollover threshold for a vehicle, explain what it does and does not capture, and relate it to NCAP ratings."
sources:
  - "NHTSA rollover resistance rating documentation (nhtsa.gov), confirm current method"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Static stability factor and rollover risk

1. Definition: `SSF = T/(2*H)` with T average track width and H CG height (both in the same units).
2. Quasi-static rollover threshold in g ~ SSF for a rigid vehicle (lateral acceleration at which the inside wheels unload fully): `ay_roll = g*T/(2*H)`. Suspension roll and tyre deflection reduce this by shifting the CG outboard; use the measured rollover threshold from a tilt-table.
3. Typical SSF values (cars above about 1.4, SUVs and pickups about 1.0-1.3) (gated: unconfirmed, source is paywalled or blocked); how NHTSA's consumer rollover rating combines SSF with a dynamic manoeuvre (gated: unconfirmed, source is paywalled or blocked) (nhtsa.gov returned 403); confirm the current method. SSF = T/(2H) and the g*T/(2H) threshold follow from the moment balance on a rigid vehicle.
4. Increase stability: widen track, lower CG, add stiffer anti-roll to reduce roll, tyre selection.
5. Stability at the limit is not just threshold: tripped rollovers (sliding into kerbs) depend on friction and lateral velocity.

**Gotchas:** CG height must include load and be measured, not estimated.

## Verify
- [ ] CG height measured by a tilt/pendulum method.
- [ ] Rollover threshold comparison between formula and tilt-table.
