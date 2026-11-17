---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.eps-assist-curve-design
name: eps-assist-curve-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [eps-assist, eps, electric-power-steering, boost-curve, assist-torque, active-return, damping-compensation]
level: practitioner
status: gated
description: "Design EPS assist: speed-dependent boost curves, return-to-centre and damping compensation, torque ripple, thermal and fail-safe limits."
sources:
  - "Pfeffer and Harrer, Steering Handbook"
  - "supplier EPS application guides (e.g. ZF, JTEKT, Bosch)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# EPS assist curve design

1. Base assist: motor torque as function of driver (column) torque, with a family of curves by vehicle speed; highest boost at parking speed, least on motorway.
2. Dead band around zero for on-centre stability; slope sets effort.
3. Active return: add torque proportional to steering angle to help centring, scaled by speed and steering velocity.
4. Damping: add a torque opposing steering velocity to avoid unwanted oscillation, higher at speed.
5. Friction and inertia compensation: reduce the perceived friction and rack inertia effects.
6. Torque ripple and noise: limit motor current ripple, avoid assist-caused steering vibrations.
7. Limits: motor current and temperature derate gradually, with a driver warning; the functional safety concept (ISO 26262; confirm clauses in the current edition (gated: unconfirmed, source is paywalled or blocked)) defines failure behaviour such as loss of assist handled safely. Steering equipment is also type-approved (UN R79); qualified functional-safety engineers own this.
8. Tune subjectively and with objective on-centre and parking tests.

**Gotchas:** instability from high boost gain with column compliance; check with frequency response.

## Verify
- [ ] Parking effort and highway effort meet targets.
- [ ] Fault-injection tests show defined safe degradation.
