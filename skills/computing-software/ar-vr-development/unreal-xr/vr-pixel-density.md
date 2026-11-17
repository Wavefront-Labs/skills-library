---
id: computing-software.ar-vr-development.unreal-xr.vr-pixel-density
name: vr-pixel-density
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, vr-pixel-density]
level: advanced
status: draft
description: "Trade resolution against GPU cost."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tune pixel density
**Goal:** Trade resolution against GPU cost.

- Console variable `vr.PixelDensity <value>` scales the eye buffer relative to the recommended size (1.0 default).
- Use dynamic resolution where supported.
- Pair with fixed foveated rendering on mobile.

## Gotchas
- Raising density without budget causes dropped frames, which is worse than blur.

## Self-check
Frame time stays under budget at the chosen density.
