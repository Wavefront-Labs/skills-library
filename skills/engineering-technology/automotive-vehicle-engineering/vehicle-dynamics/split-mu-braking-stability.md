---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.split-mu-braking-stability
name: split-mu-braking-stability
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [split-mu-braking, split-mu, abs, yaw-moment-buildup, select-low, braking-stability]
level: practitioner
status: gated
description: "Assess braking stability on a split-friction surface: yaw moment build-up, ABS select-low versus individual control, steering intervention."
sources:
  - "Limpert, Brake Design and Safety"
  - "Bosch Automotive Handbook (ABS chapters)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Split-mu braking stability

1. Setup: one side wet/ice, other asphalt (a split-mu strip) with brake from 80-100 km/h in a straight line.
2. Mechanism: high-friction side wheels generate more brake force than the low side, creating a yaw moment; the low-mu wheel locks first and ABS releases there.
3. ABS strategies (textbook content from Bosch/Limpert; not re-checked (gated: unconfirmed, source is paywalled or blocked)): **select-low** on the rear axle (limit both wheels to the lower side) for stability; front wheels individually controlled with **yaw moment build-up delay (GMB)** so the driver has time to counter-steer; plus optional steering assist.
4. Geometry that helps: negative scrub radius, small kingpin offset, so that the unbalanced braking force gives a stabilising steering torque.
5. Metrics: yaw rate and lateral deviation, stopping distance, driver steering correction required.
6. Tune with ABS supplier calibration: pressure build rates, thresholds.

**Gotchas:** extremely short stops conflict with stability; pick targets by market.

## Verify
- [ ] Measure yaw rate and deviation: remain within lane width for an unaided driver.
- [ ] Stopping distance penalty versus uniform-mu documented.
