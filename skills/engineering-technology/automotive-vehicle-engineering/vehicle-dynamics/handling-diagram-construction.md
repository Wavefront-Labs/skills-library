---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.handling-diagram-construction
name: handling-diagram-construction
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [handling-diagram, understeer, oversteer, steady-state, cornering-limit, bundorf]
level: practitioner
status: draft
description: "Build a handling diagram from front and rear axle lateral force curves and read understeer, oversteer and limit balance directly from it."
sources:
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
  - "Pacejka, Tire and Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Handling diagram construction

1. For each axle, get lateral force vs slip angle (two tyres, with load transfer included) so you can express axle lateral acceleration `ay_axle = Fy_axle/(m_axle)` as a function of slip angle.
2. Steady-state needs the same `ay` at both axles (moment balance). Using the bicycle model: `delta - L/R = alpha_f - alpha_r`. Plot `alpha_f - alpha_r` against `ay`: that curve is the handling curve.
3. Slope at origin = understeer gradient; where slope turns negative the car becomes oversteer; the highest `ay` reached is the cornering limit.
4. Which axle saturates first: compare the front and rear normalised force curves; the one hitting its maximum at lower slip is the limit axle.
5. Use to test design changes: shift weight or roll stiffness, plot new curve, compare.

**Gotchas:** diagram is quasi-steady; transient and driveline effects need simulation.

## Verify
- [ ] Linear-range slope equals the understeer gradient computed from cornering stiffness.
- [ ] Limit ay and limiting axle agree with a skidpad test.
