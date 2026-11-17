---
id: computing-software.computer-graphics-engineering.rendering-techniques.light-prepass-deferred-lighting
name: light-prepass-deferred-lighting
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, efficient-shading, light-prepass, deferred-lighting, inferred-lighting, deferred-shading, mobile-rendering]
level: practitioner
status: draft
description: "Understand light pre-pass (deferred lighting): thin normal/roughness pass, light accumulation buffer, second material pass, and when it beats full deferred."
sources: ["https://diaryofagraphicsprogrammer.blogspot.com/2008/03/light-pre-pass-renderer.html", "https://www.realtimerendering.com/", "https://advances.realtimerendering.com/s2009/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Light pre-pass and deferred lighting variants

## 1. Light pre-pass (Engel 2008) / deferred lighting
1. **Geometry pass 1**: write a thin G-buffer: depth + normal + specular power/roughness (one RGBA8
   target).
2. **Lighting pass**: for each light, accumulate diffuse and specular *lighting* (not shaded
   colour) into a light buffer: RGB = diffuse light, A = specular intensity (monochrome) or separate
   targets for coloured specular.
3. **Geometry pass 2**: re-render all opaque geometry with full materials, sampling the light buffer
   at the pixel and combining with albedo, specular colour, emissive.

## 2. Why it existed
- Small G-buffer: fits hardware with few MRTs or low bandwidth (Xbox 360/PS3 era, early mobile).
- Material variety in pass 2 (any shader can combine lighting differently).
- MSAA easier than full deferred (thin buffer).
Costs: geometry rendered twice (vertex cost and draw calls); specular colour approximations
(monochrome specular accumulation).

## 3. Variants
- **Inferred lighting** (Kircher & Lawrance 2009): light buffer at lower resolution with
  discontinuity-sensitive filtering (DSF) using object/normal IDs; transparents lit via stippling.
- **Forward+ / tiled forward**: the modern successor in spirit: depth prepass + light culling per
  tile + forward shading with full materials; no light accumulation buffer.
- **Deferred lighting on mobile with framebuffer fetch / subpasses**: keep G-buffer in tile memory
  (Vulkan subpasses, Metal imageblocks), making full deferred cheap on tilers.

## 4. Choosing today
| Situation | Pick |
|---|---|
| Many lights, complex materials, desktop | deferred or visibility buffer |
| MSAA required, varied materials | forward+ (clustered) |
| Tile-based mobile | deferred within one render pass (subpasses) or forward+ |
| Legacy/low MRT hardware | light pre-pass |

## Gotchas
- Pass 2 must render identical depth to pass 1 (same vertex shader math, `invariant gl_Position`) or
  EQUAL depth test fails with z-fighting.
- Monochrome specular in the light buffer looks wrong with coloured lights on metals.

## Verify
- [ ] Depth EQUAL test in pass 2 covers every pixel (no holes).
- [ ] Compare against forward reference for a scene with coloured lights.
