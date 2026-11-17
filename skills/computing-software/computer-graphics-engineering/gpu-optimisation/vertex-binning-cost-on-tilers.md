---
id: computing-software.computer-graphics-engineering.gpu-optimisation.vertex-binning-cost-on-tilers
name: vertex-binning-cost-on-tilers
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, binning, geometry-cost, position-only-shading, mobile-gpu, vertex-shading, lod]
level: practitioner
status: draft
description: "Control geometry cost on tile-based GPUs: binning bandwidth from vertex outputs, position-only shading, triangle density limits, LODs and index/vertex attribute compression."
sources: ["https://developer.arm.com/documentation/101897/latest/Vertex-shading", "https://developer.arm.com/documentation/102662/latest/", "https://developer.qualcomm.com/sites/default/files/docs/adreno-gpu/developer-guide/gpu/overview.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vertex binning and geometry cost on tilers

## 1. Why geometry is expensive on tilers
In the binning phase, every vertex's outputs (position + varyings) are written to memory per
primitive list, then read back for each tile the primitive touches. Cost is proportional to
vertex count x output size x tiles touched. High-poly scenes can be bandwidth-bound in geometry.

## 2. Position-only / index-driven shading
Modern Malis (Bifrost/Valhall IDVS) split the vertex shader: positions computed first for binning
and culling; varyings computed only for visible primitives. To benefit:
- Keep position computation independent and cheap; don't make position depend on varyings' inputs
  unnecessarily.
- Use separate position attribute streams (non-interleaved position buffer) so binning reads only
  positions.

## 3. Budgets and practices (Arm guidance)
- Aim for fewer than ~1 vertex per ~10 screen pixels for scene geometry; avoid micro-triangles
  (< 10 px area): they waste binning, rasterisation and quad shading.
- LODs aggressively by screen size; impostors for distant objects.
- Back-face culling on; let the hardware cull off-screen primitives early (frustum culling on CPU
  for whole objects first).
- Index buffers with good vertex reuse (meshoptimizer `optimizeVertexCache`), 16-bit indices.

## 4. Attribute compression
- Positions: fp16 or SNORM16 with per-mesh scale/offset where precision allows.
- Normals/tangents: octahedral or `A2B10G10R10_SNORM`.
- UVs: fp16/UNORM16.
Smaller input means less fetch bandwidth; smaller outputs (mediump varyings) mean less binning
bandwidth.

## 5. Measure
Arm Streamline: non-fragment (vertex/tiling) active cycles, tiler primitive counts, external
read/write bandwidth in the binning phase; Mali Offline Compiler for position vs varying shader
cycles.

## Gotchas
- Tessellation and geometry shaders are very costly on tilers; avoid.
- Huge draw counts of tiny meshes add per-draw tiler overhead; batch.

## Verify
- [ ] Vertex/primitive counts per frame within budget; micro-triangle debug view clean.
- [ ] Non-fragment cycles a minor part of frame time.
