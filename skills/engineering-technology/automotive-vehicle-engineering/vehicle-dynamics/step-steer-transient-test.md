---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.step-steer-transient-test
name: step-steer-transient-test
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [step-steer-test, step-steer, iso-7401, transient-response, yaw-response, response-time, overshoot]
level: practitioner
status: gated
description: "Perform a step-steer test and extract yaw-rate response time, peak response time, overshoot and steady-state gain with clean steering inputs."
sources:
  - "ISO 7401 (lateral transient response test methods), confirm current edition"
  - "Gillespie, Fundamentals of Vehicle Dynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Step-steer transient test

1. Choose a test speed (e.g. 80-100 km/h) and a step amplitude that gives about 0.3-0.4 g steady lateral acceleration in a linear range; use a steering robot or fast operator input. ISO 7401 specifies the method; the 50% time-zero and 90% response-time definitions below follow it (gated: unconfirmed, source is paywalled or blocked); confirm the current edition for tolerances.
2. Instrument: steering angle, yaw rate, lateral acceleration, roll, speed; sample at 100 Hz or more; low-pass filter consistently.
3. Align time zero at the point the steering angle reaches 50% of its final value.
4. Extract: **response time** = time for yaw rate to reach 90% of its final steady value; **peak response time** = time to maximum; **overshoot** = (peak - steady)/steady; steady yaw gain = steady yaw rate / steering angle.
5. Repeat left and right, several runs, average.

**Gotchas:** slow steering ramps distort response time; sign conventions; speed drop during the test.

## Verify
- [ ] Left/right and repeat runs scatter within a stated tolerance.
- [ ] Steady yaw gain matches the steady-state test at the same speed.
