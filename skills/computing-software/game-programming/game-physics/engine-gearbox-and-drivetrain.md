---
id: computing-software.game-programming.game-physics.engine-gearbox-and-drivetrain
name: engine-gearbox-and-drivetrain
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, drivetrain, vehicle-physics, engine-torque-curve, game-programming]
level: practitioner
status: verified
description: "Simulate a car drivetrain: engine torque curve, clutch, gearbox ratios, differential splits and coupling engine RPM to wheel speed stably."
sources: ["https://www.asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html", "https://jrouwe.github.io/JoltPhysics/class_wheeled_vehicle_controller.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Engine, gearbox and drivetrain simulation

**Goal:** a vehicle whose acceleration, gear shifts and engine sound come from one coherent model
(Marco Monster, *Car Physics for Games*).

## Chain
```text
throttle -> engine torque T(rpm) * throttle -> clutch -> gearbox ratio g -> final drive d
         -> differential -> wheel torque -> tire forces
wheel torque = T_engine * g * d * efficiency (Monster uses 0.7, calling it a guess; up to 30% of energy lost)
engine rpm   = wheel angular speed * g * d * 60 / (2*pi)   (when clutch engaged)
```

## Engine
- Torque curve as a lookup table (rpm -> Nm) from real data; idle rpm, redline, rev limiter.
- Engine braking: negative torque when throttle is 0, proportional to rpm.
- Engine inertia matters when the clutch is disengaged (revving in neutral).

## Gearbox and clutch
- Ratios like 3.5, 2.1, 1.4, 1.0, 0.8, reverse -3.2; final drive 3-4 (Monster's Corvette C5 example: first gear 2.66,
  fourth 1.0, differential 3.42, so a 9.1x multiplier in first).
- Shifting: disengage the clutch briefly (tune per game); automatic shifting at upshift/downshift rpm thresholds
  with hysteresis.
- Clutch as a torque-limited coupling between engine and gearbox shaft; solve the two rotational
  speeds as a constraint (like a joint motor with max torque) rather than an explicit spring, or it
  oscillates at high gear ratios.

## Differential
- Open: equal torque, wheels may spin at different speeds (inside wheel spin-out).
- Locked: equal speeds.
- Limited-slip: limit torque bias ratio. Jolt's `WheeledVehicleControllerSettings` provides
  `mDifferentials` (`VehicleDifferentialSettings::mLimitedSlipRatio`, default 1.4; `FLT_MAX` gives an open differential) and
engine/transmission settings.

## Stability
- Integrate engine and wheel angular velocities together, implicitly coupled, at the physics step
  (or substep); explicit coupling at high gear ratios explodes.

## Verify
- 0-100 km/h time and top speed per gear match a reference spreadsheet of torque and ratios.
