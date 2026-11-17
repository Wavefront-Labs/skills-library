---
id: computing-software.ar-vr-development.unreal-xr.vr-teleport-locomotion
name: vr-teleport-locomotion
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-vr-interaction-locomotion, vr-teleport-locomotion]
level: practitioner
status: draft
description: "Teleport the pawn using navigation projection."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Implement teleport locomotion
**Goal:** Teleport the pawn using navigation projection.

- Use a projectile path trace from the controller and `ProjectPointToNavigation`; teleport with a fade and `TeleportTo`.
- Build a NavMesh in the level.
- Offer snap rotate as part of the comfort setup.

## Gotchas
- Teleporting the pawn without compensating for the HMD offset places the head wrong.

## Self-check
Teleport lands on the aimed floor location.
