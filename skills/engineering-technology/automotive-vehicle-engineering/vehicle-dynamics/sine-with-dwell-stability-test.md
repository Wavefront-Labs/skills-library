---
id: engineering-technology.automotive-vehicle-engineering.vehicle-dynamics.sine-with-dwell-stability-test
name: sine-with-dwell-stability-test
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-dynamics
tags: [sine-with-dwell, esc-test, fmvss-126, un-r140, stability-test, yaw-rate-ratio]
level: practitioner
status: verified
description: "Plan and analyse a sine-with-dwell manoeuvre used for ESC verification: steering input, scaling, metrics and what to check in current regulations."
sources:
  - "FMVSS 126 and UN Regulation 140 (ESC) overview; confirm the current texts"
  - "NHTSA ESC research reports"
  - "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-571/subpart-B/section-571.126"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Sine-with-dwell stability manoeuvre

1. The manoeuvre is a sinusoidal steering input (about 0.7 Hz) with a pause (dwell, about 0.5 s) at the peak of the second half-cycle, increasing amplitude over a series of runs, run at 80 km/h entry. FMVSS 126 (eCFR text fetched): 0.7 Hz, 500 ms dwell starting at the second peak, entry at 80 +/- 2 km/h coasting in high gear; A is the steering wheel angle giving 0.3 g from six Slowly Increasing Steer runs; runs start at 1.5A and step by 0.5A to the greater of 6.5A or 270 deg (300 deg cap). Confirm the same in UN R140 / the local rule.
2. Scale steering amplitude from a slowly increasing steer test at 80 km/h to find the angle that gives 0.3 g, then use multiples of that angle.
3. Metrics assessed by the regulations: yaw-rate decay after the steering reversal (a fraction of peak after a set time) and lateral displacement of the vehicle centre of mass at a set time after steering starts. FMVSS 126 limits (eCFR S5.2): yaw rate no more than 35% of the first peak at 1.0 s after completion of steer and 20% at 1.75 s; lateral displacement of the CG at least 1.83 m (GVWR up to 3,500 kg) or 1.52 m (above) at 1.07 s after beginning of steer, for runs of 5A or more. Surface peak friction coefficient 1.02 (ASTM F2493 tyre), ambient 7-40 C. Other markets/editions: look them up.
4. Use a steering robot for repeatability; run with ESC on and off to see ESC benefit.
5. Check tyre condition and test surface per the standard; report ambient and surface friction.

**Gotchas:** wrong sign conventions for yaw sign, incorrectly scaled amplitude, driver steering instead of robot.

## Verify
- [ ] Amplitude sequence reaches the highest angle required by the protocol.
- [ ] Yaw-rate ratios and displacement computed per the protocol's time references.
