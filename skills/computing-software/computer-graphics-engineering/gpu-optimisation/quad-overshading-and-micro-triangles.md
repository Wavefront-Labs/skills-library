---
id: computing-software.computer-graphics-engineering.gpu-optimisation.quad-overshading-and-micro-triangles
name: quad-overshading-and-micro-triangles
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, fragment-cost, quad-overshading, micro-triangles, helper-lanes, lod, quad-overdraw-view]
level: sme
status: draft
description: "Diagnose and fix small-triangle costs: 2x2 quad overshading, helper lanes, rasteriser throughput limits, quad-overdraw views, and LOD/meshlet fixes."
sources: ["https://www.realtimerendering.com/", "https://blog.selfshadow.com/publications/overdraw-in-overdrive/", "https://gpuopen.com/learn/rdna-performance-guide/", "https://developer.nvidia.com/blog/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Small triangles and quad overshading

## 1. Why tiny triangles are expensive
- Pixel shaders run in 2x2 quads so derivatives (`ddx/ddy`, texture LOD) work. A triangle covering 1 pixel
  still launches a full quad: 3 helper lanes wasted, 4x shading cost. Triangles covering a few pixels each
  typically waste 50-75% of pixel shader work.
- Rasterisers emit a limited number of triangles per clock and setup costs per triangle; below ~10 px per
  triangle, the front end becomes the bottleneck regardless of shader cost.
- Long thin triangles (slivers) touch many quads with little coverage each.

## 2. Measure
- **Quad overdraw view**: count quads shaded per pixel with an atomic add in a debug shader, or the built-in
  views (Unreal "Quad Overdraw" / "Shader Complexity & Quads", RenderDoc overlay "Quad Overdraw (Pass)").
- Profilers: Nsight "Pixel Shader Helper Threads" / warp occupancy by helper lanes; RGP wavefront occupancy
  with partially covered waves; PIX "% quads with coverage".
- Triangle size histogram: total covered pixels / triangles drawn per mesh.

## 3. Fixes
1. **LOD**: target ~10-20 px per triangle on screen (see LOD selection skill); screen-size-based LOD switching.
2. **Avoid slivers**: mesh simplification and remeshing that maximise minimum angle; fan triangulation of
   circles (caps, wheels) is the classic offender - use strips or max-area triangulation.
3. **Visibility buffer / deferred texturing**: rasterise IDs cheaply, shade once per pixel in compute.
4. **Software rasterisation for micro-polygons** (Nanite approach): compute-shader raster for clusters
   whose triangles are smaller than a pixel.
5. Deferred shading already moves heavy lighting to full-screen passes; only the G-buffer pass pays overshading.
6. Distant foliage: impostors/billboards instead of dense geometry.

## Gotchas
- MSAA amplifies the problem in some cases (more coverage samples, more partially covered quads).
- Helper lanes still execute loops and texture fetches; heavy shaders on dense meshes are the worst case.
- `discard` in helper lanes is not allowed to change derivatives; avoid early returns before derivative use.

## Verify
- [ ] Quad overdraw view mostly 1-2 on dense meshes after LOD; pixel shader time drops in the GPU capture.
