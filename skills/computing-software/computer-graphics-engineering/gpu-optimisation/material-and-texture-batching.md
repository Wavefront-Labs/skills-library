---
id: computing-software.computer-graphics-engineering.gpu-optimisation.material-and-texture-batching
name: material-and-texture-batching
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, cpu-overhead, texture-batching, material-batching, texture-arrays, bindless, srp-batcher, draw-calls]
level: practitioner
status: draft
description: "Reduce material and texture switches: texture arrays and atlases, bindless descriptors, shared material parameter buffers, and SRP Batcher-style constant layouts."
sources: ["https://docs.unity3d.com/Manual/SRPBatcher.html", "https://vkguide.dev/docs/gpudriven/gpu_driven_engines/", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/resource-binding-in-hlsl"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Material and texture batching

## 1. Why
Changing textures or material constants between draws forces descriptor/binding updates and
prevents merging draws into instanced or indirect batches.

## 2. Texture arrays and atlases
- **Texture2DArray** for textures of the same size/format: one binding, slice index per
  material/instance. Mipmapping and wrap modes work per slice (unlike atlases).
- **Atlases**: pack many small textures; needs padding, no wrapping, mip bleeding care.
- Group materials by size/format to fill arrays.

## 3. Bindless
All textures live in one large descriptor table/heap; shaders index by material ID:
```hlsl
Texture2D gTextures[] : register(t0, space1);         // unbounded array (SM 5.1+)
float4 c = gTextures[NonUniformResourceIndex(mat.albedoIdx)].Sample(s, uv);
// SM 6.6: ResourceDescriptorHeap[mat.albedoIdx]
```
Vulkan: descriptor indexing (`runtimeDescriptorArray`, `PARTIALLY_BOUND`, `UPDATE_AFTER_BIND`) or
descriptor buffers. Mark non-uniform indices (`NonUniformResourceIndex` / `nonuniformEXT`) when
the index can vary within a wave, or results are undefined.

## 4. Material parameters
- Store all materials' constants in one structured buffer; draws carry a material index (push
  constant / instance data).
- Unity **SRP Batcher**: materials keep persistent GPU constant buffers with identical layouts per
  shader variant; per-draw only the object buffer changes, so draws with different materials but the
  same shader variant are cheap. Keep `UnityPerMaterial` CBUFFER layout identical across passes.

## 5. Result
With bindless + material buffers + instanced/indirect draws, a whole scene can render with a handful
of draws per pipeline (GPU-driven rendering).

## Gotchas
- Divergent bindless indices within a wave cost extra on some GPUs (scalarisation loops).
- Texture arrays require same dimensions and mip counts: resizing assets may lose quality.
- Atlases break hardware wrap and anisotropic filtering at borders.

## Verify
- [ ] Draw/state change counts drop in captures; frame CPU time measured before/after.
- [ ] No visual differences from atlasing (bleeding) at distance.
