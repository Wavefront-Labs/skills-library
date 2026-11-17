---
id: computing-software.ar-vr-development.unity-xr.xr-hands-package-joints
name: xr-hands-package-joints
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-hands, xr-hands-package-joints]
level: advanced
status: draft
description: "Use the XR Hands subsystem to read joint poses."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read hand joints with XR Hands
**Goal:** Use the XR Hands subsystem to read joint poses.

- Install com.unity.xr.hands; enable the Hand Tracking Subsystem feature in the OpenXR settings.
- Use XRHandSubsystem and `XRHand.GetJoint(XRHandJointID.IndexTip).TryGetPose(out pose)`.
- Use the XR Hand Skeleton Driver / XR Hand Mesh Controller to visualise.

## Gotchas
- Joint poses are relative to the XR Origin; handle tracking loss.

## Self-check
Skeleton visible and following the real hand on a hand-tracking device.
