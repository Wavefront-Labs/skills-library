---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-audio-room-acoustics
name: xr-audio-room-acoustics
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-audio-room-acoustics]
level: advanced
status: draft
description: "Add reverb and occlusion that match the virtual or real space."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Add room acoustics
**Goal:** Add reverb and occlusion that match the virtual or real space.

- Use reverb zones or a room-acoustics SDK; in AR use scene meshes for occlusion where supported.
- Keep budgets low on standalone devices.
- Check loudness across headsets.

## Gotchas
- Heavy reverb reduces speech intelligibility.

## Self-check
Dialogue stays clear at all listening positions.
