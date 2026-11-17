---
id: computing-software.computer-graphics-engineering.rendering-techniques.shadow-atlas-and-shadow-caching
name: shadow-atlas-and-shadow-caching
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, shadows, shadow-atlas, shadow-caching, local-light-shadows, shadow-mapping, texture-atlas]
level: advanced
status: draft
description: "Manage many shadowed lights with a shadow atlas: allocation by screen size, quadtree/packing, caching static shadows and updating only when lights or casters move."
sources: ["https://docs.unity3d.com/Packages/com.unity.render-pipelines.high-definition@17.0/manual/Shadows-in-HDRP.html", "https://docs.unrealengine.com/5.3/en-US/shadowing-in-unreal-engine/", "https://www.activision.com/cdn/research/2017_DD_Rendering_of_COD_IW.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shadow atlases and caching

## 1. Atlas basics
One large depth texture (e.g. 4096^2 or 8192^2 D16/D32) holds shadow maps for many spot and point
lights (point = 6 faces or 2 paraboloid/octahedral regions). Each light gets a rectangle; shaders
get a per-light `atlasScaleOffset` to transform shadow UVs.

## 2. Allocation
- Resolution per light from its projected screen size / importance:
  `res = clamp(nextPow2(screenRadiusPx * k), 64, 1024)`.
- Pack with a quadtree (power-of-two squares; simple, fast to free) or a shelf/skyline packer.
- Re-allocate each frame from scratch for dynamic budgets, or keep stable slots for cached lights.
- Add a 1-2 texel border (or clamp UVs in the shader) so PCF doesn't sample neighbours.

## 3. Caching
Rendering shadows for dozens of lights every frame is expensive. Cache:
- **Static lights with static casters**: render once; re-render only on invalidation.
- **Static + dynamic split**: cached static depth copied into the slot each frame, then dynamic
  casters drawn on top (HDRP "mixed cached shadows", UE "shadow map caching").
- Invalidate when: light moves/changes, a static caster within the light's bounds moves, the slot
  resolution changes.
- Time-slice updates: N lights per frame, round-robin by priority; distant lights update less often.

## 4. Point lights
Cube faces in the atlas: 6 rects, sample with a face-select function (major axis) and per-face
matrices. Cull faces whose frustum doesn't intersect the view frustum or contain casters.

## 5. Filtering in an atlas
Hardware comparison sampling (`sampler2DShadow`) with bilinear PCF works; wide PCF kernels must be
clamped to the rect to avoid bleeding.

## Gotchas
- Changing a light's resolution between frames makes shadows pop; hysteresis on resolution choice.
- Atlas fragmentation with variable sizes: periodically defragment or rebuild.
- Depth bias depends on texel size; scale bias per light resolution.

## Verify
- [ ] Atlas debug view: no overlaps, borders intact.
- [ ] Shadow rendering time scales with number of invalidated lights, not total lights.
