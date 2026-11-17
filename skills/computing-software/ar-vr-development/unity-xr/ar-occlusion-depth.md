---
id: computing-software.ar-vr-development.unity-xr.ar-occlusion-depth
name: ar-occlusion-depth
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-ar-occlusion-meshing, ar-occlusion-depth]
level: advanced
status: draft
description: "Enable AROcclusionManager for depth-based occlusion."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Occlude virtual content with environment depth
**Goal:** Enable AROcclusionManager for depth-based occlusion.

- Add AROcclusionManager to the AR Camera, set Environment Depth Mode and Occlusion Preference Mode; use shaders or the occlusion material support in URP.
- Feature is device dependent (ARCore Depth API, ARKit LiDAR).
- Fall back gracefully with no occlusion.

## Gotchas
- Depth is lower resolution than colour; edges look soft.

## Self-check
A virtual cube hides behind a real table edge.
