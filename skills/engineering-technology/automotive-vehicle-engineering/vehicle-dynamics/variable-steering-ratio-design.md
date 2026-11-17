---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.variable-steering-ratio-design
name: variable-steering-ratio-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [steering-ratio, variable-ratio, steering-rack, lock-to-lock, overall-ratio, vgr, steering-design]
level: practitioner
status: gated
description: "Choose overall steering ratio and its variation: lock-to-lock turns, rack tooth pitch variation, and speed-dependent software ratio, with package limits."
sources:
  - "Pfeffer and Harrer, Steering Handbook"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Variable steering ratio

1. Overall ratio = steering wheel angle / road wheel angle. Typical road cars are around 13-18:1, with 2.5-3.2 turns lock-to-lock (gated: unconfirmed, source is paywalled or blocked); sports cars toward the lower end, large vehicles higher; benchmark.
2. Components: rack travel per pinion revolution (mm/rev) and steering arm geometry set the ratio. A rack with varying tooth pitch gives variable ratio (quicker off-centre).
3. Targets: parking effort/turns at low speed, response at high speed, turning circle.
4. Check kinematics: Ackermann, bump steer and compliance change effective ratio; verify with the actual steering system.
5. Speed-dependent ratio (steer-by-wire or active steering) needs the functional safety case and regulation compliance.
6. Measure with a steering robot: plot wheel angle vs steering wheel angle at several loads.

**Gotchas:** variable pitch with EPS assist changes torque too; re-tune assist.

## Verify
- [ ] Ratio curve measured on vehicle matches design within tolerance.
- [ ] Turning circle and lock-to-lock turns meet targets.
