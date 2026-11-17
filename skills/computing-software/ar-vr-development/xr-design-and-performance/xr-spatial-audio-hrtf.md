---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-spatial-audio-hrtf
name: xr-spatial-audio-hrtf
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-spatial-audio, xr-spatial-audio-hrtf]
level: practitioner
status: draft
description: "Make sounds localisable in 3D."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use spatialised audio with HRTF
**Goal:** Make sounds localisable in 3D.

- Use the engine's spatialiser (platform or third-party SDK) with HRTF, distance attenuation and optional occlusion.
- Keep music and UI non-spatial; spatialise important cues.
- Profile CPU cost of voices.

## Gotchas
- Spatialisation of stereo assets mixes poorly; author sources as mono.

## Self-check
Closing your eyes you can point to a sound's source.
