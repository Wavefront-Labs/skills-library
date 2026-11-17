---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.magnetorquers-and-detumble
name: magnetorquers-and-detumble
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [magnetorquers, detumble, b-dot, magnetic-torque-rods, momentum-dumping, adcs]
level: practitioner
status: draft
description: "Size magnetorquers, implement B-dot detumbling and magnetic momentum unloading, and handle the underactuated geometry and residual dipole."
sources:
  - "Markley and Crassidis, Fundamentals of Spacecraft Attitude Determination and Control"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Magnetorquers and detumble

**Goal:** use Earth's field to damp initial tumbling and unload reaction wheels.

## Physics
Torque `tau = m x B`, with `m` the commanded dipole (A m^2) and `B` the local field. In low Earth orbit `B` is of the order of 20 to 50 microtesla (check with a field model such as IGRF), so torque is small: a dipole of 1 A m^2 gives roughly 3e-5 N m. Torque is always perpendicular to `B`, so no torque is available along the field direction at any instant; the orbital motion changes `B`'s direction and gives full-axis control over time.

## B-dot detumble
1. Measure `B` in the body frame (magnetometer); estimate `B_dot` by differencing and filtering.
2. Command `m = -k * B_dot`, with `k` chosen from the orbit and inertia; saturate the dipole.
3. Detumbling takes from minutes to a few orbits depending on size and gain.
4. Turn off torquing during magnetometer reads (time-multiplex) to avoid coil-field corruption.

## Momentum unloading
- Wheel momentum is dumped by commanding `m` so that `tau = m x B` opposes the stored momentum: `m = k * (B x h_error)/|B|^2` (cross-product law).

## Sizing
1. Disturbance torque, wheel momentum growth per orbit, or detumble rate target.
2. Required dipole `m = tau / B_min` with margin; typical small satellites use dipoles of the order of 0.1 to a few A m^2.
3. Power: coil resistance gives watts at the commanded current.

## Gotchas
- Residual spacecraft dipole disturbs attitude; measure and compensate.
- At high inclination the field geometry limits torque near the equator.
- Sign errors in magnetometer axes cause detumble to accelerate rotation.

## Verify
- [ ] A simulation from a high initial rate with noisy `B` converges to below the target rate in the planned time.
