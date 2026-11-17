---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.intent-recognition
name: intent-recognition
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [intent-recognition, locomotion-mode-recognition, gait-phase-detection, terrain-recognition, powered-prosthesis-control]
level: advanced
status: draft
description: "Design locomotion intent recognition for powered prostheses and exoskeletons: sensor inputs, gait phase and mode classifiers, latency, error cost and safe fallbacks."
sources: ["Journal literature on locomotion mode recognition for powered lower limb prostheses (confirm citations)", "IEC 62304 and ISO 14971 for software risk", "https://www.ieee.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Locomotion intent recognition

**Goal:** detect what the user is about to do (walk, stairs, ramp, sit, stand) fast and reliably enough to switch control safely.

## Inputs
- Embedded IMU, load cell, joint angle and pressure sensors; EMG from residual muscles; sometimes environment sensing (camera, depth).
- Gait phase estimated from the shank angle or thigh angle trajectories, load and timing.

## Methods
1. **Rule-based or finite state machines** with thresholds: simple, interpretable and predictable; need tuning per user.
2. **Machine learning classifiers** (linear discriminant analysis, support vector machines, neural networks) on windowed features from several sensors; train on labelled data from the user or a group; check generalisation across users and terrain.
3. **Phase variables** (continuous gait phase) provide smooth control without discrete modes.
4. Latency budget: decisions must precede the step transition (tens to a couple of hundred milliseconds); measure end-to-end.

## Safety
- The cost of a misclassification is a stumble. Define the error severity per mode pair (mistaking stair for level is worse than the reverse), use confidence thresholds, hold previous safe mode when unsure, and allow a manual override.
- Verify with stress tests: slow gait, stop-start, uneven terrain, sensor dropouts.
- Software lifecycle and risk files apply (IEC 62304 and ISO 14971).

## Verify
- [ ] Classification accuracy and confusion matrix reported per mode.
- [ ] Latency measured end to end.
- [ ] Failsafe behaviour tested for sensor failure and low confidence.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
