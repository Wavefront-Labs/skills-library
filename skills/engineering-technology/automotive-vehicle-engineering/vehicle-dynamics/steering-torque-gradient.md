---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.steering-torque-gradient
name: steering-torque-gradient
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [steering-torque-gradient, steering-torque, torque-gradient, steering-effort, lateral-acceleration, steering-feel]
level: practitioner
status: draft
description: "Measure and tune steering wheel torque versus lateral acceleration, understand the contributions of tyre aligning moment and assist, and set targets."
sources:
  - "Pfeffer and Harrer, Steering Handbook"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Steering torque gradient

1. Measure: constant-radius or slow-ramp steer test with a steering torque sensor; plot column torque vs lateral acceleration.
2. Components: tyre aligning moment (pneumatic trail times lateral force), mechanical trail (caster), friction, EPS assist. Aligning moment peaks before the lateral force peaks and then falls, which signals approaching the limit to the driver.
3. Gradient: slope in N m per g at low lateral acceleration (the on-centre/linear range), and the level at 0.3-0.5 g. Benchmark competitors; targets vary by segment.
4. Tune: caster and trail (hardware), EPS boost curve (software), tyre choice (aligning stiffness), rack friction.
5. Make sure torque still rises as lateral acceleration grows to 0.5-0.6 g so the driver feels the build-up, then falls gently near limit.

**Gotchas:** assist applying too much boost in mid-range numbs the feel; measure with assist on at representative temperature.

## Verify
- [ ] Gradient and level documented at 0.1, 0.3 and 0.5 g and compared with benchmark.
- [ ] Torque falls near the limit instead of continuing to rise.
