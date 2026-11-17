---
id: computing-software.ar-vr-development.unreal-xr.motioncontroller-component-hands
name: motioncontroller-component-hands
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-vr-pawn-motion-controllers, motioncontroller-component-hands]
level: practitioner
status: draft
description: "Attach controllers to the pawn with the MotionController component."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use MotionControllerComponent
**Goal:** Attach controllers to the pawn with the MotionController component.

- Add a MotionController component per hand, set Motion Source to Left or Right.
- Parent under a VROrigin scene component beneath the pawn; camera also under VROrigin.
- Render a mesh or the platform controller model attached to it.

## Gotchas
- Parenting the controller outside VROrigin offsets it from the player.

## Self-check
Hands track and follow the pawn when moving.
