---
id: computing-software.game-programming.game-engine-architecture.draw-call-submission-and-batching
name: draw-call-submission-and-batching
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, draw-call-batching, sort-keys, render-queue, instancing, indirect-draw, state-changes, game-programming]
level: advanced
status: draft
description: "Design draw submission: render queues with 64-bit sort keys, minimising state changes, instancing and merging, bindless and indirect draws, and measuring CPU submit cost."
sources: ["https://realtimecollisiondetection.net/blog/?p=86", "https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/indirect-drawing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Draw call submission and batching

**Goal:** submit thousands of objects per frame with low CPU cost: fewer API calls, fewer state
changes, and work moved to the GPU where possible.

## Render queue with sort keys (Ericson "Order your graphics draw calls around!")
Each visible item emits a compact draw packet plus a 64-bit **sort key**; sort keys, then submit.
```
| layer/viewport 4b | pass 4b | translucency 2b | depth 24b (front-to-back opaque, back-to-front translucent) |
| material/shader id 20b | mesh id 10b |
```
- Opaque: sort by shader/material first (fewer pipeline/descriptor switches), depth second for
  early-z; or depth first after a depth prepass.
- Translucent: back-to-front depth first (correct blending), material second.
- Radix sort of 64-bit keys is fast and stable; keys can be built in parallel per job.
- Submission loop compares the previous packet's state and only binds what changed.

## Reduce draw count
- **Instancing:** same mesh + material, per-instance buffer of transforms (vegetation, crowds, debris).
- **Static merging/batching:** combine static meshes sharing a material offline (costs memory and
  culling granularity).
- **Texture arrays / atlases / bindless** descriptors so different textures do not split batches;
  material parameters in a big structured buffer indexed per draw.
- **GPU-driven rendering:** cull on the GPU and emit `ExecuteIndirect` / `vkCmdDrawIndexedIndirectCount`
  arguments; with mesh/meshlet clusters (Aaltonen & Haar, SIGGRAPH 2015) one call draws the scene.

## Cost model
In D3D11/GL, per-draw driver overhead dominated (a few thousand draws per frame). In D3D12/Vulkan
draws are cheaper but pipeline (PSO) changes, descriptor updates and resource barriers still cost;
record command lists in parallel per pass/thread.

## Engine mapping
Unity: SRP Batcher, GPU instancing, static batching, GPU Resident Drawer / BatchRendererGroup (see
unity `srp-batcher-and-gpu-instancing`). Unreal: auto-instancing of static meshes, mesh draw command
caching, ISM/HISM, Nanite (GPU-driven clusters). Godot: MultiMesh, automatic 2D batching.

## Measure
CPU: render-thread time and draw/PSO-change counts (RenderDoc, PIX, `stat RHI`, Frame Debugger).
GPU: whether the pass is vertex/fragment bound (batching does not fix GPU-bound frames).

## Verify
- [ ] Draw and state-change counts per pass are tracked in a stats overlay.
- [ ] Translucent ordering is correct after sorting changes (test overlapping glass).
- [ ] Doubling identical-mesh object counts barely increases CPU submit time (instancing works).
