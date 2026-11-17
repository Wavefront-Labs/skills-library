---
id: computing-software.ar-vr-development.unreal-xr.instanced-stereo-mobile-multiview
name: instanced-stereo-mobile-multiview
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, instanced-stereo-mobile-multiview]
level: advanced
status: draft
description: "Reduce draw calls by drawing both eyes together."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable Instanced Stereo or Mobile Multi-View
**Goal:** Reduce draw calls by drawing both eyes together.

- Rendering > VR > Instanced Stereo on for PC; Mobile Multi-View on for Android standalone headsets.
- Verify materials and post-process are compatible.
- Check stats with `stat unit` and `stat gpu`.

## Gotchas
- Some post-process effects are unsupported with multi-view.

## Self-check
Draw calls drop after enabling.
