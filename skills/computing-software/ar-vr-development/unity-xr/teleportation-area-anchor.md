---
id: computing-software.ar-vr-development.unity-xr.teleportation-area-anchor
name: teleportation-area-anchor
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xri-locomotion, teleportation-area-anchor]
level: practitioner
status: draft
description: "Add teleport locomotion with a Teleportation Provider."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Teleportation areas and anchors
**Goal:** Add teleport locomotion with a Teleportation Provider.

- Add a Locomotion System (or Locomotion Mediator in XRI 3) and Teleportation Provider on the XR Origin.
- Mark floors with Teleportation Area, snap points with Teleportation Anchor.
- Use a ray interactor on a separate action for teleport aim and select to confirm.

## Gotchas
- Without a Locomotion System component the provider does nothing.

## Self-check
Pointing at a floor and releasing moves the rig to that point.
