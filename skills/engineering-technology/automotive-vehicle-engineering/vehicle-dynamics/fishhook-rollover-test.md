---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.fishhook-rollover-test
name: fishhook-rollover-test
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [fishhook-test, fishhook, dynamic-rollover, two-wheel-lift, outrigger, rollover-test]
level: practitioner
status: gated
description: "Describe how to run a fishhook rollover manoeuvre: steering input, entry speed, safety outriggers, instrumentation and wheel-lift metrics."
sources:
  - "NHTSA dynamic rollover test procedure documents (nhtsa.gov), confirm current version"
  - "SAE J2114 is the dolly rollover (tripped) recommended practice, not the fishhook; see the NHTSA fishhook documents above"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Fishhook rollover test

1. Purpose: assess on-road tripped-less rollover propensity of a vehicle through rapid steer, counter-steer with a dwell.
2. Procedure outline (details gated: unconfirmed, NHTSA documents returned 403 or unreadable PDF): steering robot applies a steering input of defined rate and amplitude, holds, then reverses at a time tied to measured roll rate or a fixed delay; entry speeds are stepped upward; the test records two-wheel lift. Exact amplitudes, rates and timing come from the current NHTSA procedure; confirm the version before testing.
3. Safety: fit outriggers, full instrumentation, remote data link, trained test driver or robot, test only on a sealed, large, flat surface.
4. Load: test at a defined loaded condition (driver, outriggers, fuel level) with CG height measured.
5. Metrics: wheel lift (height threshold as defined in the procedure), roll angle and roll rate, lateral acceleration, steering and speed.
6. Use result with SSF for ratings; use test to evaluate ESC.

**Gotchas:** outrigger inertia changes CG; treat their effect as per procedure.

## Verify
- [ ] Run log matches the specified entry speeds and steering amplitudes.
- [ ] Data include CG height, load, tyre condition and surface friction.
