---
id: computing-software.ar-vr-development.unity-xr.xr-device-simulator-testing
name: xr-device-simulator-testing
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, xr-device-simulator-testing]
level: practitioner
status: draft
description: "Use the XR Device Simulator for quick iteration."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test without a headset using the XR Device Simulator
**Goal:** Use the XR Device Simulator for quick iteration.

- Import the XR Device Simulator sample from the XR Interaction Toolkit package and add the prefab to the scene.
- Keyboard/mouse emulate head and controller movement.
- Still validate on a real device before release.

## Gotchas
- The simulator does not model tracking loss or latency.

## Self-check
Controls drive interactors in Play mode.
