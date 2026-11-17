---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.reaction-wheel-sizing
name: reaction-wheel-sizing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, adcs, attitude-control, reaction-wheels, reaction-wheel-sizing, momentum-storage, slew-rate, disturbance-torque]
level: practitioner
status: verified
description: "Size reaction wheels for slew torque and momentum storage from inertia, slew time and environmental disturbance torques, and plan desaturation."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Sidi, Spacecraft Dynamics and Control"
  - "Markley and Crassidis, Fundamentals of Spacecraft Attitude Determination and Control"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Reaction wheel sizing

**Goal:** wheel torque and momentum capacity for the mission.

## Slew requirements
For a rest-to-rest slew of angle `theta` in time `t` with a bang-bang (triangular rate) profile: angular acceleration `alpha = 4 theta/t^2`, peak rate `omega = 2 theta/t`. Torque `T = I alpha`; momentum `h = I omega`.

## Disturbance momentum
- Gravity-gradient torque: `T_gg = (3 mu/(2 R^3)) |I_z - I_y| sin(2 theta)` (`R` orbit radius, `theta` angle from local vertical).
- Other sources: aerodynamic drag (low orbits), solar radiation pressure, residual magnetic dipole, thruster misalignment.
- Cyclic disturbance over an orbit: momentum storage `h = T_d (P/4) 0.707` (SMAD form (gated: unconfirmed, source is paywalled or blocked)); secular disturbances accumulate as `h = T_d P` per orbit and need regular desaturation.

## Procedure
1. Compute inertia matrix and worst-case slew; derive torque and momentum for each axis.
2. Add margin (commonly 20-50% in early design (gated: unconfirmed, source is paywalled or blocked)) and choose a wheel (or four-wheel pyramid for redundancy) from vendor datasheets: peak torque, momentum capacity, maximum speed, power, mass.
3. Plan desaturation with magnetorquers (low orbit) or thrusters; avoid zero-speed crossings that cause torque noise.
4. Check jitter from wheel imbalance for precision-pointing payloads.

## Gotchas
- Wheel momentum is a vector sum in pyramid configurations; capacity depends on direction.
- Sustained slews drain wheel momentum; budget per-orbit momentum, not only peak.

## Verify
- [ ] Slew example: 90 degrees in 100 s gives `alpha = 6.28e-4 rad/s^2` and peak rate 0.0314 rad/s (recomputed).
