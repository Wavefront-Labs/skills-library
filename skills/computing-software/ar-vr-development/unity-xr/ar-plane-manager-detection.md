---
id: computing-software.ar-vr-development.unity-xr.ar-plane-manager-detection
name: ar-plane-manager-detection
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-ar-planes-raycasts, ar-plane-manager-detection]
level: practitioner
status: draft
description: "Enable plane detection and visualise detected planes."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detect planes with ARPlaneManager
**Goal:** Enable plane detection and visualise detected planes.

- Add ARPlaneManager with a prefab (ARPlane + mesh) and set Detection Mode (horizontal, vertical).
- Subscribe to `planesChanged` for added, updated and removed.
- Disable the manager and hide planes after placement to save power.

## Gotchas
- Plane detection is not supported on all devices; check descriptor.

## Self-check
Planes appear on tabletop surfaces.
