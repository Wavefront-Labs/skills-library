---
id: computing-software.ar-vr-development.unity-xr.xr-origin-camera-offset
name: xr-origin-camera-offset
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-origin-rig, xr-origin-camera-offset]
level: practitioner
status: draft
description: "Build the XR Origin hierarchy with the main camera and hand controllers."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set up the XR Origin rig
**Goal:** Build the XR Origin hierarchy with the main camera and hand controllers.

- GameObject > XR > XR Origin (VR) creates Camera Offset, Main Camera with Tracked Pose Driver, and left/right controllers.
- Move the player by moving the XR Origin root, never the camera.
- Keep a single camera tagged MainCamera under the offset.

## Gotchas
- Scaling the origin scales the world as perceived; avoid unless intentional.

## Self-check
Head movement shifts the camera while the origin stays fixed.
