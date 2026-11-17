---
id: computing-software.ar-vr-development.unity-xr.socket-interactor-snapping
name: socket-interactor-snapping
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, socket-interactor-snapping]
level: practitioner
status: draft
description: "Create sockets that accept specific objects."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Snap objects into XR Socket Interactors
**Goal:** Create sockets that accept specific objects.

- XR Socket Interactor with a trigger collider; tune Show Interactable Hover Meshes and Socket Active.
- Filter accepted objects with interaction layers or an XR Interaction Filter (XRI 3 select filters).
- Ensure the grabbed object's own collider does not collide with the socket body.

## Gotchas
- Starting the scene with an object inside a socket needs Starting Selected Interactable.

## Self-check
Dropping a key near the socket snaps it in place.
