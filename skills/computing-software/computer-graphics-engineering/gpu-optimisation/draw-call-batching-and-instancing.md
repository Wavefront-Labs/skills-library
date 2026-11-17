---
id: computing-software.computer-graphics-engineering.gpu-optimisation.draw-call-batching-and-instancing
name: draw-call-batching-and-instancing
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [gpu-optimisation, draw-calls, instancing, batching, gpu-driven-rendering, indirect-draw, multidraw, state-sorting, dynamic-batching, atlas, texture-array, cpu-bound, instance-buffer]
level: advanced
status: draft
description: "Cut CPU-side draw call overhead: state sorting, GPU instancing, indirect/multi-draw, and GPU-driven culling — with the numbers that tell you when it actually matters."
sources: ["https://developer.nvidia.com/blog/advanced-api-performance-indirect-draws/", "https://docs.unity3d.com/Manual/GPUInstancing.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Draw call batching and instancing

**Goal:** reduce CPU-side submission overhead and redundant state changes without
breaking correctness (depth order, per-instance variation) — and know when draw
calls aren't actually the bottleneck so you don't optimise the wrong thing.

## Is this even the problem?
Check CPU frame time breakdown first (profiler, not guesswork): if the CPU isn't
the limiter, cutting draw calls won't move the frame rate. A few thousand draw
calls on modern desktop GPUs with modern APIs (D3D12/Vulkan) is often fine if
command recording is well threaded; the "draw calls are expensive" rule of thumb
is mostly a D3D11/OpenGL legacy-API and mobile-driver-overhead story.

## State sorting
Before batching anything, sort draw calls to minimise **state changes** (pipeline/
shader, then material/textures, then vertex buffers) — a state change (especially
a full pipeline state object swap) typically costs more than the draw call
submission itself. Sort key is usually: opaque-vs-transparent → shader → material
→ depth (front-to-back for opaque to help early-Z, back-to-front for transparent
for correct blending).

## GPU instancing
When many objects share the same mesh+material and differ only by transform/colour
(foliage, crowd, debris):
```hlsl
// per-instance data in a StructuredBuffer, indexed by SV_InstanceID
StructuredBuffer<float4x4> instanceTransforms : register(t0);
float4x4 worldMat = instanceTransforms[instanceID];
```
- One draw call (`DrawInstanced`/`glDrawArraysInstanced`) submits N instances;
  per-instance data comes from a buffer indexed by instance ID rather than a
  uniform/constant per draw.
- Breaks down when instances need **different materials/textures** — texture
  arrays or atlases let you keep instancing by passing a per-instance texture
  index instead of splitting into per-texture draw calls.
- Per-instance **sorting for transparency** is lost inside a single instanced
  draw — fine for additive/opaque-ish effects (particles often accept this), wrong
  for correctly order-dependent alpha blending of large instances.

## Indirect and multi-draw
- **Indirect draw** (`DrawIndexedInstancedIndirect` / `vkCmdDrawIndexedIndirect`):
  draw arguments (instance count, etc.) come from a GPU buffer instead of the CPU
  — lets a compute shader decide what to draw (GPU-driven culling/LOD) without a
  CPU readback round-trip.
  - This is the backbone of **GPU-driven rendering**: a compute pass does frustum/
    occlusion culling and LOD selection over the whole scene, writes surviving draw
    commands into an indirect buffer, one `ExecuteIndirect`/multi-draw submits all
    of them. CPU submits a near-constant small number of commands regardless of scene size.
- **Multi-draw indirect** (`vkCmdDrawIndexedIndirectCount` / `MultiDrawIndirect`):
  batches many indirect draws (one per distinct mesh, say) into a single API call,
  further cutting CPU submission cost.

## Static vs dynamic batching
- **Static batching**: merge meshes that never move relative to each other at
  build/load time into one buffer — zero runtime cost, but increases memory
  (duplicated vertex data) and breaks per-object culling granularity.
- **Dynamic batching** (engine auto-merges small moving meshes sharing a material
  each frame): CPU cost to rebuild the batch every frame — only wins for very
  small meshes (few hundred verts); the rebuild cost exceeds the draw-call savings
  above that.

## Verify
- [ ] CPU frame time profiled and confirmed as the actual bottleneck before
      investing in batching/instancing work.
- [ ] Instanced draws checked for correct transparency ordering if any instances
      use alpha blending.
- [ ] GPU-driven culling output (indirect buffer counts) spot-checked against
      expected visible-object counts, not just "it renders something."
- [ ] State-change sort order verified by instrumenting actual pipeline/material
      switch counts, not assumed from source order.
