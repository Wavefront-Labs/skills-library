---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-eye-hand-data-privacy
name: xr-eye-hand-data-privacy
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-privacy-sensor-data, xr-eye-hand-data-privacy]
level: practitioner
status: draft
description: "Treat gaze, hand and body data as sensitive biometric-adjacent data."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handle eye, hand and body tracking data safely
**Goal:** Treat gaze, hand and body data as sensitive biometric-adjacent data.

- Collect the minimum, process on device where possible, and do not store raw gaze or hand data unless essential.
- Obtain explicit consent and state purpose; honour platform permission denial.
- Check the laws that apply to biometric data in your markets (GDPR special categories, regional biometric laws).

## Gotchas
- Gaze patterns can reveal health and attention; never send them to analytics by default.

## Self-check
Data-flow diagram shows no raw sensor data leaving the device by default.
