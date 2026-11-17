---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.roll-gradient-targets
name: roll-gradient-targets
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [roll-gradient, roll-angle, body-roll, deg-per-g, roll-stiffness, roll-target]
level: practitioner
status: gated
description: "Set and verify body roll gradient in degrees per g, balancing driver feel, camber control and ride, and calculate it from stiffness."
sources:
  - "Gillespie, Fundamentals of Vehicle Dynamics"
  - "Milliken and Milliken, Race Car Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Roll gradient targets

1. Definition: roll angle per unit lateral acceleration, deg/g, from steady cornering.
2. Computation: `phi/ay = ms*(h - hr)/(Kf + Kr - ms*g*(h - hr))` in rad per (m/s^2); multiply by 9.81 and 57.3 for deg/g.
3. Targets: passenger cars commonly roughly 3-6 deg/g; sporty cars lower. Treat as a starting range and benchmark competitors (gated: unconfirmed, source is paywalled or blocked); the gradient formula in step 2 was computed and is consistent with the roll angle in lateral-load-transfer-calculation.
4. Trade-offs: low roll gradient feels responsive but may harden ride; high roll gradient feels softer but camber in roll and lateral load shift suffer.
5. Camber in roll: use kinematics (camber per degree of roll) to ensure the loaded outside tyre keeps useful camber.
6. Verify with constant-radius test and compare with predicted.

**Gotchas:** compliance (bushings, subframe) adds roll; account for it by measurement.

## Verify
- [ ] Measured roll gradient within target band.
- [ ] Outside-tyre camber at 0.8 g within the tyre's recommended range.
