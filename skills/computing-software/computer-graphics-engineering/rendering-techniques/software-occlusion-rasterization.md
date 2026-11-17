---
id: computing-software.computer-graphics-engineering.rendering-techniques.software-occlusion-rasterization
name: software-occlusion-rasterization
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, acceleration-lod, software-occlusion, occlusion-culling, masked-occlusion-culling, simd, cpu-culling]
level: advanced
status: docs-checked
description: "Cull with a CPU software occlusion rasteriser: Intel Masked Occlusion Culling API, clip-space input, TestRect queries, interleaving, threading and precision options."
sources: ["https://github.com/GameTechDev/MaskedOcclusionCulling"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Software occlusion rasterization

## 1. Idea
Rasterise occluder meshes into a low-resolution CPU hierarchical depth buffer, then test
occludees against it. Intel's Masked Occlusion Culling (MOC) decouples depth values from
coverage and works directly on the hierarchical depth buffer, which lets it parallelise both
coverage computation and buffer updates. The internal buffer stores only two depth values and a
mask per tile. The repository is archived by Intel: no further maintenance or patches.

## 2. API essentials (from the README)
- Optimised for AVX capable CPUs, with SSE 4.1 and SSE 2 implementations; the right one is
  chosen at run time. AVX-512 support is experimental. Licence: Apache 2.0.
- Create and destroy with the static `Create()` / `Destroy()` (custom aligned allocators can be
  passed in).
- `SetResolution(w, h)`: width must be a multiple of 8 and height a multiple of 4.
- `ClearDepthBuffer()` each frame. Optional `SetNearClipPlane(dist)`, default 0.
- `RenderTriangles(verts, indices, triCount, modelToClip, backfaceWinding, clipPlaneMask, layout)`
  renders occluders. Vertices are clip-space (x, y, z, w) floats; z is ignored and depth is 1 / w.
  Only triangle lists are supported. Passing a model-to-clip matrix is typically faster than
  `TransformVertices()` first.
- Backface culling: clockwise triangles are culled by default; `BACKFACE_CCW` or no culling are
  available (modes other than `BACKFACE_CW` may be slightly slower).
- Clip flags let the caller skip clipping planes, but wrongly disabling one can crash or read
  out of bounds. Use `CLIP_PLANE_ALL` when in doubt.
```cpp
MaskedOcclusionCulling* moc = MaskedOcclusionCulling::Create();
moc->SetResolution(640, 360);
moc->ClearDepthBuffer();
moc->RenderTriangles(verts, indices, triCount, nullptr, MaskedOcclusionCulling::BACKFACE_CW);
auto r = moc->TestRect(xmin, ymin, xmax, ymax, wmin);   // NDC rect plus clip-space w
bool visible = (r == MaskedOcclusionCulling::VISIBLE);
```

## 3. Queries
- `TestTriangles()` is like `RenderTriangles()` but does not update the buffer. Results are
  `VISIBLE`, `OCCLUDED` or `VIEW_CULLED` (all triangles frustum or backface culled).
- `TestRect()` takes normalised device coordinates (x/w, y/w in [-1,1]) plus the clip-space w.
  It is considerably faster than `TestTriangles()` (no input assembly, clipping or
  rasterisation) and less accurate because screen-space rectangles grow large; the authors saw
  best overall performance with this type of culling. The application computes the projected
  bounding rectangle.

## 4. Render order and interleaving
- Front-to-back occluder order improves both quality and speed, because early depth tests run
  during occluder rendering.
- Occluder rendering and queries can be interleaved cheaply: after drawing the first occluders,
  start querying, and skip drawing an occluder mesh whose object was found occluded. This can
  give early exits in BVH traversal.
- Two update heuristics: `QUICK_MASK` (default, speed) and not defining it (the merging
  heuristic from "Masked Depth Culling for Graphics Hardware": more accurate, less leakage,
  slower). Leakage of background through foreground in the depth visualisation is part of the
  algorithm.
- Depth buffers can be merged (added May 2018), which helps parallel construction and reduces
  silhouette bleed when input cannot be roughly sorted front to back, for example terrain
  patches with foreground occluders.

## 5. Precision and threading
- `PRECISE_COVERAGE` enables Bresenham-interpolated rasterisation following DirectX 11 and
  OpenGL rules, 5-15 percent slower. `USE_D3D` (default on) selects y-down screen space.
- Threading uses a binning rasteriser (`BinTriangles()`, `RenderTrilist()` with a scissor
  rectangle from `ComputeBinWidthHeight()`). `CullingThreadpool` is an example task system with
  asynchronous occluder rendering; queries may run against an out-of-date buffer, which stays
  conservative (occluded objects may be reported visible, not the reverse). `Flush()` waits for
  workers. The authors measured roughly 3x on four threads in their interleaved BVH traversal.
- `ComputePixelDepthBuffer()` produces a per-pixel buffer for visualisation; `ENABLE_STATS`
  gives counters.

## Gotchas
- A near plane of 0 is the default; set it if on-screen geometry is clipped by the near plane in
  the main renderer.
- Build times are long due to heavy inlining; compile a library file or disable whole-program
  optimisation for the MOC source files.

## Verify
- [ ] Debug overlay of the software depth buffer matches scene silhouettes.
- [ ] No false-occlusion popping in a scripted flythrough; draw count reduction logged.

## Checked

Method: docs-checked 2026-11-09 against the full MaskedOcclusionCulling README on GitHub (raw markdown, read in full). Dropped the Intel article and GDC links (not read), Frostbite/Killzone attributions, the 8x4 tile and 640x360 budget figures, the occluder-count advice and the "shrink occluders" guidance.
