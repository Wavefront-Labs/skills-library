---
id: computing-software.ar-vr-development.unity-xr.grab-interactable-attach
name: grab-interactable-attach
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-xri-interactables, grab-interactable-attach]
level: practitioner
status: draft
description: "Make an object grabbable with correct attach transforms and throw behaviour."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configure XR Grab Interactable
**Goal:** Make an object grabbable with correct attach transforms and throw behaviour.

- Add Rigidbody, Collider and XR Grab Interactable; set Movement Type (Instantaneous, Kinematic, VelocityTracking).
- Use an Attach Transform child so the held pose matches the hand; tick Track Position/Rotation as needed.
- Throw On Detach and Throw Velocity Scale control release velocity.

## Gotchas
- Wrong Movement Type causes jitter or objects tunnelling through walls.

## Self-check
Pick up, rotate and throw an item without jitter.
