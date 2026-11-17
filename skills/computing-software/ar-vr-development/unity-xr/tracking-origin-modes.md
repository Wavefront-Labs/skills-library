---
id: computing-software.ar-vr-development.unity-xr.tracking-origin-modes
name: tracking-origin-modes
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, tracking-origin-modes]
level: practitioner
status: draft
description: "Set the tracking origin mode so height is correct."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Floor versus device tracking origin
**Goal:** Set the tracking origin mode so height is correct.

- On XR Origin set Tracking Origin Mode to Floor (camera Y offset is zero) or Device (use Camera Y Offset for a seated eye height).
- Recenter with the XRInputSubsystem `TryRecenter` when the platform supports it.
- Some devices ignore the requested mode; check `TrySetTrackingOriginMode` result.

## Gotchas
- A wrong mode puts the player under or above the floor.

## Self-check
A cube placed at Y=0 rests on the real floor in Floor mode.
