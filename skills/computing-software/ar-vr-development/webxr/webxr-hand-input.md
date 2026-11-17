---
id: computing-software.ar-vr-development.webxr.webxr-hand-input
name: webxr-hand-input
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-hand-input]
level: advanced
status: draft
description: "Read joints through the Hand Input module."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use WebXR hand input
**Goal:** Read joints through the Hand Input module.

- Request the 'hand-tracking' feature; `inputSource.hand` is an XRHand with 25 joints keyed by name.
- `frame.getJointPose(joint, refSpace)` returns pose and radius.
- Use pinch distance for selection.

## Gotchas
- Support depends on the browser and device.

## Self-check
Joint spheres track your fingers.
