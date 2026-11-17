---
id: computing-software.game-programming.game-engine-architecture.gpu-driven-rendering
name: gpu-driven-rendering
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, gpu-driven-rendering, indirect-draw, gpu-culling, game-programming]
level: practitioner
status: draft
description: "Move culling and draw submission to the GPU: instance buffers, compute frustum and occlusion culling, indirect multi-draw, meshlets and bindless resources."
sources: ["https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/indirect-drawing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU-driven rendering

**Goal:** render hundreds of thousands of objects with near-zero CPU cost by letting the GPU decide
what to draw (Aaltonen and Haar, *GPU-Driven Rendering Pipelines*, SIGGRAPH 2015).

## Pipeline
1. **Scene data on GPU:** instance buffer (transform, bounds, mesh id, material id) uploaded once,
   updated incrementally for moving objects.
2. **Compute culling:** per instance (or per cluster/meshlet), test frustum and occlusion against a
   hierarchical Z-buffer (HZB) built from last frame's depth or a depth pre-pass.
3. **Compaction:** surviving instances appended to a visible list with an atomic counter; write
   draw arguments.
4. **Indirect draw:** `ExecuteIndirect` (D3D12), `vkCmdDrawIndexedIndirectCount` (Vulkan),
   `multiDrawIndexedIndirect`; one call draws everything sharing a pipeline.
5. **Bindless materials:** shaders index texture/material arrays by id, so state changes don't split draws.

## Two-phase occlusion
Phase 1: draw objects visible last frame, build HZB. Phase 2: test the rest against new HZB, draw
newly visible ones. Avoids one-frame popping from last-frame HZB.

## Meshlets / clusters
Split meshes into ~64-128 triangle clusters with bounds and normal cones; cull clusters (backface
cone, frustum, occlusion). Mesh shaders (D3D12 Ultimate, Vulkan `VK_EXT_mesh_shader`) process
meshlets directly. Unreal Nanite extends this with cluster LOD hierarchies and software rasterisation.

## Requirements and pitfalls
- Uniform vertex formats/mega buffers so draws can share bindings.
- Debuggability: visualise culling results; read back counters for stats.
- Transparent objects still need sorting (often CPU or separate GPU sort).

## Verify
- CPU render time flat while instance count grows 10x; GPU capture shows culling compute and few
  indirect draws.
