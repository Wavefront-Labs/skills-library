---
id: computing-software.computer-graphics-engineering.rendering-techniques.surfel-and-radiance-cache-gi
name: surfel-and-radiance-cache-gi
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, surfel-gi, radiance-cache, lumen, gibs, screen-probes, world-space-probes]
level: sme
status: draft
description: "Understand surfel-based and radiance-cache GI (EA GIBS, Lumen-style): surfel spawning and lifetime, irradiance caching, screen probes, world radiance cache and their trade-offs."
sources: ["https://www.ea.com/seed/news/siggraph21-global-illumination-surfels", "https://advances.realtimerendering.com/s2022/SIGGRAPH2022-Advances-Lumen-Wright%20et%20al.pdf", "https://advances.realtimerendering.com/s2021/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Surfel and radiance-cache GI

## 1. Surfel GI (EA SEED GIBS, 2021)
- **Surfels** = small surface discs spawned on screen-visible geometry where coverage is lacking
  (screen-space coverage test per tile), attached to (possibly moving) meshes.
- Each surfel accumulates irradiance by tracing a few rays per frame (ray tracing) with
  multi-bounce through querying other surfels at hits; moments-based temporal accumulation.
- Spatial acceleration: surfels hashed into a camera-centred grid/cascade; lighting lookup gathers
  surfels overlapping the pixel, weighted by distance and normal.
- Recycling: surfels not seen for a while are destroyed; budget fixed (e.g. 64-256K surfels).
Pros: GI detail adapts to visible geometry; works with dynamic objects. Cons: complexity,
requires RT.

## 2. Lumen-style radiance caching (UE5)
Layers (simplified):
1. **Screen probes**: adaptive probes placed on the GBuffer (every 16 px plus extra where needed);
   each traces rays (screen-space first, then software/hardware RT against SDFs or triangles).
2. **Hit lighting** from a **surface cache** (cards capturing material and lighting of meshes) so
   hits are cheap.
3. **World-space radiance cache**: sparse clipmap of probes that long rays sample instead of
   tracing all the way, giving multi-bounce and stabilising distant lighting.
4. Importance sampling of probe rays from previous frame's radiance and BRDF; spatial and temporal
   filtering of probes; integrate to pixels with bent normals.

## 3. Why caches
Per-pixel path tracing is too expensive at real-time sample counts; caches reuse radiance across
pixels and frames. The design question is where (screen, surface, world) and at what resolution.

## 4. Trade-offs
| Approach | Strength | Weakness |
|---|---|---|
| Probe grid (DDGI) | simple, robust | leaks, low detail |
| Surfels | geometry-adaptive | complex bookkeeping |
| Screen probes + world cache | detail where you look, scalable | very complex, lag under fast changes |

## Gotchas
- All caches lag: fast light changes (flashlights, explosions) need direct paths or faster
  hysteresis in affected regions.
- Thin geometry and interiors stress any cache (leaks); invest in visibility (moments, SDF tracing).

## Verify
- [ ] Indirect lighting stable (no crawling) while the camera moves slowly.
- [ ] Response time to a light toggle measured and within design target.
