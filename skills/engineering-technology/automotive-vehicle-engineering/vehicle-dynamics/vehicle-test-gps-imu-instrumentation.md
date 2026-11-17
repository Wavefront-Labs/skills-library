---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.vehicle-test-gps-imu-instrumentation
name: vehicle-test-gps-imu-instrumentation
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [vehicle-test-instrumentation, gps, imu, ins, lever-arm, iso-8855, data-logging]
level: practitioner
status: gated
description: "Instrument a vehicle for dynamics testing with GNSS/INS, steering and wheel sensors: mounting, lever-arm corrections, axis conventions and calibration."
sources:
  - "ISO 8855 (vehicle dynamics vocabulary), ISO 15037-1 (general conditions, passenger cars), confirm editions"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# GPS and IMU instrumentation

1. Axes: ISO 8855 vehicle axes (x forward, y left, z up (gated: unconfirmed, source is paywalled or blocked)); write down the sign conventions for yaw, roll, pitch.
2. Mount the IMU rigidly near the CG or on a stiff cross-member; measure the offset vector (lever arm) from CG, and apply the correction in the software.
3. GNSS: use RTK/INS units for ground-speed, slip angle and position (accuracy per the unit's datasheet (gated: unconfirmed, source is paywalled or blocked)); set antenna lever arms; wait for solution lock before runs.
4. Sensors: steering wheel angle/torque, wheel speeds, suspension displacement, pedal positions, brake pressure.
5. Sample at 100 Hz or higher, time-synchronise all channels (common clock or PTP), anti-alias filter before decimating.
6. Calibrate: zero offsets on level ground, steering angle with a steering robot or protractor, roll/pitch via a flat surface test.
7. Check sensor-derived sideslip against a reference at slow speed on a steady-state test.

**Gotchas:** vibration contaminating accelerometers; GNSS dropouts under trees/bridges.

## Verify
- [ ] Static zero and tilt checks pass before each session.
- [ ] Lever-arm correction validated on a slow circle (acceleration at CG matches).
