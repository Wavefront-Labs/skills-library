---
id: engineering-technology.biomedical-engineering.biomechanics.imu-gait-analysis
name: imu-gait-analysis
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [imu-gait, inertial-sensors, wearable-gait, sensor-fusion, zero-velocity-update]
level: advanced
status: draft
description: "Estimate gait events, spatiotemporal parameters and segment angles from IMUs: placement, sampling, event detection, drift control, zero-velocity updates and validation."
sources: ["Sabatini et al., Assessment of walking features from foot inertial sensing (IEEE Trans Biomed Eng, 2005)", "Winter and Sabatini literature on inertial gait analysis (confirm citations)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Inertial sensor gait analysis

**Goal:** measure gait outside the lab with wearable IMUs while knowing the error sources.

## Setup
- **Placement:** foot or shank sensors give events and stride length; pelvis (lower back) gives step regularity; thigh and shank pairs give joint angles. Fix sensors firmly (straps, no skin-slide) and record orientation relative to the segment.
- **Sampling:** 100 Hz is common for walking; use higher (about 200 Hz or more) for running or sharp impacts; range of gyroscope and accelerometer must not saturate in the foot.

## Processing
1. **Orientation:** sensor-fusion filter (complementary or Kalman) of gyroscope, accelerometer and optionally magnetometer; magnetometers are disturbed by steel and electronics indoors, so many gait systems limit their use.
2. **Events:** heel strike and toe off from foot angular velocity (the swing peak and the following near-zero periods) or shank signals.
3. **Stride length:** strapdown integration of acceleration after removing gravity, with a **zero-velocity update (ZUPT)** at each mid-stance that resets velocity drift; integrate between stance phases.
4. **Segment-to-sensor calibration:** a standing pose or functional movements to align sensor axes to anatomy.
5. Drift: integrated errors grow with time; use update steps and report error accumulation.

## Validation
- Compare with a marker-based system or instrumented walkway; report bias, limits of agreement, and reliability (ICC) for each parameter.

## Verify
- [ ] Sensor placement and orientation documented per participant.
- [ ] Event timing error versus reference estimated.
- [ ] Stride length error stated for the walking speeds studied.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
