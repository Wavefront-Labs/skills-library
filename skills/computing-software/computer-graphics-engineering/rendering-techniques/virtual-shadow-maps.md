---
id: computing-software.computer-graphics-engineering.rendering-techniques.virtual-shadow-maps
name: virtual-shadow-maps
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, shadows, virtual-shadow-maps, sparse-shadow-maps, page-tables, clipmap-shadows]
level: sme
status: draft
description: "Implement virtual shadow maps: very high resolution sparse shadow maps with per-page allocation, clipmap levels for directional lights, caching and invalidation."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/virtual-shadow-maps-in-unreal-engine", "https://ktstephano.github.io/rendering/stratusgfx/svsm", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Virtual shadow maps

**Idea:** one huge virtual shadow texture (e.g. 16K x 16K per light or per clipmap level) split
into pages (128x128); only pages that visible pixels need are allocated and rendered.

## 1. Frame flow
1. **Mark**: from the depth buffer, project each pixel into light space, pick the clipmap level
   (directional) or mip (local lights) by screen-space texel density, and mark the needed page in
   a page-request buffer.
2. **Allocate**: compact requests; map virtual pages to physical pages in a pool texture
   (e.g. 8K x 8K physical); update the page table (virtual page -> physical page, flags).
3. **Render**: draw shadow casters only into newly needed or invalidated pages; cull geometry per
   page (GPU-driven, meshlets) and use the page table in the vertex/mesh shader to route
   triangles to physical tiles.
4. **Sample**: shade with page-table lookup, then the physical texel; fall back to a coarser
   level if a page is missing.

## 2. Directional lights: clipmaps
Levels doubling in world coverage centred on the camera, snapped to page size to avoid shimmer.
Each level reuses pages as the camera moves (only the leading edge renders).

## 3. Caching
Static geometry pages stay cached across frames; invalidate pages touched by moving objects
(their bounds projected into page space). Separate static and dynamic layers if many movers.

## Gotchas
- Without GPU-driven culling, re-rendering many pages is too expensive; this design assumes
  mesh/cluster culling.
- Filtering across page boundaries: sample in physical space only within a page; PCF kernels need
  borders or per-tap page lookups.
- Memory spikes on camera cuts (everything invalid); cap pages per frame and degrade.

## Verify
- [ ] Page visualisation: allocated pages hug visible geometry; shadow cost stable when static.
