---
id: computing-software.ar-vr-development.unreal-xr.unreal-ar-trackables-pins
name: unreal-ar-trackables-pins
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-ar-trackables-pins]
level: advanced
status: draft
description: "Respond to planes and keep content anchored with AR Pins."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Work with AR trackables and pins
**Goal:** Respond to planes and keep content anchored with AR Pins.

- Use AR Trackable Notify and Get All Geometries; line-trace against AR with `Line Trace Tracked Objects`.
- Pin actors with `Pin Component` so they follow tracking updates.
- Handle tracking state changes.

## Gotchas
- Unpinned actors drift when tracking updates.

## Self-check
Placed actor stays fixed on a table.
