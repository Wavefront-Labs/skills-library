---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.combined-slip-friction-ellipse
name: combined-slip-friction-ellipse
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [combined-slip, friction-ellipse, friction-circle, traction-circle, longitudinal-lateral, tyre-behaviour]
level: practitioner
status: gated
description: "Estimate available lateral force while braking or accelerating using the friction ellipse, and recognise its limits against full combined-slip models."
sources:
  - "Pacejka, Tire and Vehicle Dynamics"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Combined slip and the friction ellipse

1. Simple model: `(Fx/Fx_max)^2 + (Fy/Fy_max)^2 <= 1`. With equal limits it is the friction circle: total force magnitude <= mu*Fz.
2. Use: if a wheel delivers `Fx` of braking, remaining lateral force `Fy = Fy_max*sqrt(1 - (Fx/Fx_max)^2)`. Braking at 80% of limit leaves ~60% lateral.
3. Real tyres are not exactly elliptical: peak lateral often exceeds peak longitudinal or vice versa (gated: unconfirmed, source is paywalled or blocked), so use separate maxima and a shape check from test data.
4. For accuracy use a combined-slip model (Magic Formula with weighting functions, or a brush model) that works in slip angle and slip ratio, not forces.
5. Application: ABS/ESC logic, trail-braking analysis, brake-in-turn stability limit, traction control targets.

**Gotchas:** the ellipse ignores slip-speed coupling and the difference between forces at the same total slip; use as sketch-level design tool only.

## Verify
- [ ] Locked-wheel (Fx at maximum) gives near-zero lateral force in test or model.
- [ ] Ellipse vs full model difference quantified at two or three combinations.
