---
id: computing-software.ar-vr-development.unity-xr.xr-input-system-action-maps
name: xr-input-system-action-maps
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xr-input-actions, xr-input-system-action-maps]
level: practitioner
status: draft
description: "Use Input Action assets with XR controller paths."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bind XR controllers with Input Actions
**Goal:** Use Input Action assets with XR controller paths.

- Bind to `<XRController>{LeftHand}/trigger` or the OpenXR paths from the chosen profile; XRI ships a default action asset (XRI Default Input Actions).
- Enable the actions (an Input Action Manager, or by enabling asset references) or nothing is read.
- Use Tracked Pose Driver with an InputAction for position/rotation.

## Gotchas
- Disabled actions return zero silently.

## Self-check
Input Debugger shows control values changing when pressing the trigger.
