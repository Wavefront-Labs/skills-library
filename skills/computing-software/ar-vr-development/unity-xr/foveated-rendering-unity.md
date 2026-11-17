---
id: computing-software.ar-vr-development.unity-xr.foveated-rendering-unity
name: foveated-rendering-unity
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, foveated-rendering-unity]
level: advanced
status: draft
description: "Reduce shading cost in peripheral vision."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable foveated rendering
**Goal:** Reduce shading cost in peripheral vision.

- Unity exposes a Foveated Rendering API (`XRDisplaySubsystem.foveatedRenderingLevel`, and `foveatedRenderingFlags` for gaze) on supporting devices.
- Fixed foveated rendering (lower resolution at edges) is common on standalone headsets; eye-tracked versions need eye tracking permission.
- Confirm device support in the provider docs.

## Gotchas
- Aggressive levels show visible edge artefacts on text.

## Self-check
GPU frame time drops measurably after enabling.
