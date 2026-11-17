---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.star-tracker-and-attitude-sensors
name: star-tracker-and-attitude-sensors
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [star-tracker, attitude-sensors, sun-sensor, gyroscope, attitude-determination, adcs]
level: practitioner
status: draft
description: "Select and integrate star trackers, sun sensors, magnetometers and gyros for attitude determination, with accuracy, exclusion-angle and fusion considerations."
sources:
  - "Wertz, Spacecraft Attitude Determination and Control"
  - "Markley and Crassidis, Fundamentals of Spacecraft Attitude Determination and Control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Star trackers and sensors

**Goal:** a sensor suite that meets knowledge accuracy through all mission modes.

## Sensor types
- **Star tracker**: images stars, matches to a catalogue, outputs a quaternion; best accuracy (arcseconds to tens of arcseconds), with cross-boresight error larger than the roll-about-boresight error in many designs (check the datasheet; roll error is typically worse than the cross-boresight error for a single head).
- **Sun sensors**: coarse or fine; used for safe mode and checks.
- **Magnetometers**: coarse attitude in LEO from the field model; low cost.
- **Earth horizon sensors**: nadir direction.
- **Gyros** (MEMS, fibre-optic, hemispherical resonator): rate propagation between star tracker updates; bias and noise matter (angle random walk, bias instability).

## Integration
1. Allocate error budget: sensor noise, alignment, thermal distortion between sensor and payload, and estimator error.
2. Placement: sun, Moon and Earth limb exclusion angles (tens of degrees; take from the datasheet) must stay clear in all attitudes; use two heads if coverage requires it.
3. Slew limits: star tracker lost-in-space acquisition needs low rate; tracking mode tolerates higher rates (see datasheet).
4. Fusion: an extended Kalman filter (multiplicative form for quaternions) combines gyro propagation with star tracker updates and estimates gyro bias.
5. Fall-back modes for sun in view, eclipse, and sensor failure.

## Gotchas
- Alignment calibration on orbit (star-tracker to body) is a common correction.
- Thermal distortion of the mounting bracket can dominate the budget.
- Radiation and proton hits create noise in the detector; check recovery behaviour.

## Verify
- [ ] The end-to-end pointing knowledge budget, from analysis or hardware-in-the-loop simulation, meets the requirement with margin in each mode.
