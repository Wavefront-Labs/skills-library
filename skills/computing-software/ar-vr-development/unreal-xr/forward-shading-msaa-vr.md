---
id: computing-software.ar-vr-development.unreal-xr.forward-shading-msaa-vr
name: forward-shading-msaa-vr
category: computing-software
field: ar-vr-development
product: unreal-xr
tags: [unreal-xr, unreal-vr-rendering-settings, forward-shading-msaa-vr]
level: advanced
status: draft
description: "Switch to forward rendering for performance and MSAA in VR."
sources: ['https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-xr-experiences-in-unreal-engine']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use forward shading with MSAA
**Goal:** Switch to forward rendering for performance and MSAA in VR.

- Project Settings > Rendering: Forward Shading on, Anti-Aliasing Method MSAA.
- Confirm the project loses deferred-only features (such as some screen-space effects).
- Restart the editor after changing.

## Gotchas
- Features such as DBuffer decals and SSR work differently in forward; test your content.

## Self-check
Edges are crisp with no TAA ghosting in-headset.
