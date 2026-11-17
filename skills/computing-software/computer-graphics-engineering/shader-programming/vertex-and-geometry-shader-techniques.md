---
id: computing-software.computer-graphics-engineering.shader-programming.vertex-and-geometry-shader-techniques
name: vertex-and-geometry-shader-techniques
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [shader-programming, vertex-shader, geometry-shader, tessellation-shader, mesh-shader, skinning, vertex-pulling, gpu-skinning, lod, tessellation, hull-shader, domain-shader, amplification-shader]
level: advanced
status: docs-checked
description: "Vertex pipeline techniques beyond basic transforms: GPU skinning, vertex pulling, tessellation (hull/domain), geometry shaders, and why mesh shaders are replacing both on modern hardware."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/MeshShader.md", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#limits", "https://registry.khronos.org/vulkan/specs/latest/man/html/VK_EXT_mesh_shader.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vertex and geometry shader techniques

**Goal:** know the vertex-pipeline stages beyond "transform and pass through,"
and which of the older stages (geometry shaders) have real performance traps
that make mesh shaders the modern replacement for their use cases.

## GPU skinning
- Classic: vertex shader reads bone indices + weights (up to 4 bones typically,
  sometimes 8 for high-quality facial rigs) from vertex attributes, blends bone
  matrices (`skinMatrix = Σ weight_i * boneMatrix_i`), transforms position and
  normal by the blended matrix.
- **Normal/tangent skinning** needs the same blended matrix's inverse-transpose
  in principle, but in practice most engines just reuse the blended matrix
  directly for normals (acceptable since bone matrices are typically rigid/
  near-rigid, not heavily scaled) — breaks visibly if a bone has significant
  non-uniform scale.
- Bone matrices live in a buffer (UBO/SSBO/StructuredBuffer) indexed per-draw or
  per-instance — large character counts favour **GPU-based skinning in a compute
  pre-pass** (skin once, write to a buffer, reuse for shadow+main+other passes)
  over re-skinning per pass in the vertex shader, avoiding redundant blend work.

## Vertex pulling
Instead of fixed vertex-attribute binding (input layout), fetch vertex data
manually from a `StructuredBuffer`/SSBO indexed by `SV_VertexID` / `gl_VertexIndex` (`gl_VertexID` in OpenGL):
- Decouples vertex format from the fixed-function input-assembler, enabling
  flexible/compact/quantized vertex formats, bindless-style access to multiple
  meshes' data from one shader, and easier integration with GPU-driven rendering
  (the compute culling pass can write vertex/index references directly, no IA
  state changes needed per draw).
- Costs a layer of indirection the IA's dedicated hardware doesn't have — profile
  before switching a whole pipeline; the win is architectural flexibility, not
  guaranteed raw throughput.

## Tessellation (hull/domain shaders)
- **Hull shader**: per-patch, decides tessellation factor (how finely to
  subdivide) — typically driven by screen-space edge length or distance to
  camera, so detail scales with how much screen space a patch actually covers.
- **Domain shader**: runs per generated vertex after tessellation, computes
  final position (e.g. displacement mapping — sample a height map to push the
  newly generated vertex along the normal).
- **Cracks between patches** at differing tessellation factors are the classic
  bug — adjacent patches with mismatched edge tessellation leave gaps; fix with
  consistent edge-factor calculation shared between neighbouring patches (factor
  based on the shared edge, not each patch independently).

## Geometry shaders: use sparingly
- Run once per primitive, can emit 0, 1, or many output primitives — used for
  billboard/particle expansion (point → quad), wireframe-on-shaded overlays,
  single-pass cubemap rendering (emit to 6 faces via layered rendering).
- Geometry shaders have a declared maximum output (Vulkan guarantees `maxGeometryOutputVertices` of at least 256).
  They are often a poor fit for large amplification; profile before using one for any high-primitive-count case.

## Mesh shaders (modern replacement)
- Mesh shaders (Direct3D 12, Vulkan `VK_EXT_mesh_shader`) replace the
  vertex/hull/domain/geometry pipeline with a compute-like model: an optional
  **amplification/task shader** decides how much work to generate, a **mesh
  shader** outputs a small cluster of vertices+primitives directly, with full
  access to groupshared memory and compute-style flexibility.
- This is the usual replacement for geometry-shader amplification —
  used for GPU-driven culling-per-cluster (meshlets), procedural geometry, and
  replacing tessellation's fixed pipeline with programmable subdivision.
  Check device support at runtime and keep a vertex/compute fallback path.

## Verify
- [ ] Skinning normal transform checked for correctness if any bone uses
      non-uniform scale (visible as pinched/stretched normals under skinning).
- [ ] Tessellation edge factors shared/consistent between adjacent patches,
      checked visually for cracks at varying LOD distances.
- [ ] Geometry shader usage profiled and confirmed not a bottleneck, or replaced
      with mesh shaders/instancing on hardware that supports it.
- [ ] Vertex pulling's indirection overhead benchmarked against fixed-function IA
      before committing a whole pipeline to it.

## Checked

Checked 2026-10-26 against DirectX-Specs MeshShader.md (main) and Vulkan-Docs limits chapter (main, 2026-10-23). Confirmed: the D3D12 mesh shader design (amplification shader stage plus mesh shader replacing the vertex pipeline); `VK_EXT_mesh_shader` name; `maxGeometryOutputVertices` minimum 256; Vulkan GLSL uses `gl_VertexIndex`. The skinning, vertex-pulling and tessellation-crack guidance is general technique and was not checked against a primary source. Removed as unconfirmed: the 'notoriously slow' geometry shader claim (now 'profile'), the named GPU generations for mesh shader support, 'DX12 Ultimate' branding.

Method: documentation only; no commands were run.
