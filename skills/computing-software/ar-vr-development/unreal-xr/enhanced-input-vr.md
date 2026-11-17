---
id: computing-software.ar-vr-development.unreal-xr.enhanced-input-vr
name: enhanced-input-vr
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, enhanced-input-vr]
level: practitioner
status: draft
description: "Map controller buttons to Input Actions."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bind VR input with Enhanced Input
**Goal:** Map controller buttons to Input Actions.

- Create Input Actions and a Mapping Context; bind to keys named by the OpenXR profile (e.g. Left Trigger, Left Thumbstick Y).
- Add the mapping context in BeginPlay via the Enhanced Input subsystem.
- Use Value types appropriate to axes.

## Gotchas
- Forgetting to add the mapping context silently drops input.

## Self-check
Print String fires on trigger press.
