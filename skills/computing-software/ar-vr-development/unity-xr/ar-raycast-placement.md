---
id: computing-software.ar-vr-development.unity-xr.ar-raycast-placement
name: ar-raycast-placement
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, ar-raycast-placement]
level: practitioner
status: draft
description: "Place objects on detected surfaces with a screen raycast."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Place content with ARRaycastManager
**Goal:** Place objects on detected surfaces with a screen raycast.

- `arRaycastManager.Raycast(touch.position, hits, TrackableType.PlaneWithinPolygon)`; use hits[0].pose.
- Instantiate once, then move the instance on later taps.
- Add an AR Anchor to keep the object stable (see anchors).

## Gotchas
- Screen-to-world raycasts need an AR Camera tagged correctly.

## Self-check
Tapping a plane places the prefab on it.
