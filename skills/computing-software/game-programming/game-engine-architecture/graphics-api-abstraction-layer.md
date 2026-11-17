---
id: computing-software.game-programming.game-engine-architecture.graphics-api-abstraction-layer
name: graphics-api-abstraction-layer
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, rhi, graphics-abstraction, d3d12, vulkan, game-programming]
level: practitioner
status: draft
description: "Design a render hardware interface over D3D12, Vulkan and Metal: resource and pipeline objects, command lists, barriers, descriptor models and leaky abstractions."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/render-dependency-graph-in-unreal-engine", "https://github.com/NVIDIA-RTX/NRI"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Graphics API abstraction layer (RHI)

**Goal:** one renderer, several backends (D3D12, Vulkan, Metal, console APIs), without lowest-common-
denominator performance.

## Abstraction level
Abstract at the level of modern explicit APIs, not D3D11-style state:
- **Resources:** buffers, textures, views; created from descriptors (size, format, usage flags).
- **Pipelines:** full PSOs (shaders + raster/blend/depth state + formats) created up front.
- **Command lists:** recorded on any thread, submitted to queues (graphics, compute, copy).
- **Synchronisation:** fences/timeline semaphores for CPU-GPU and cross-queue sync.
- **Binding:** descriptor sets/tables or bindless indices.

Examples: Unreal RHI under RDG, The Forge, NVIDIA NRI, Diligent Engine, SDL_GPU, wgpu/WebGPU (a
portable API in itself).

## Barriers
Expose resource state transitions explicitly, or have a render graph compute them from declared
reads/writes (preferred: per-pass declarations produce optimal barriers and aliasing).

## Shaders
Author in HLSL, compile with DXC to DXIL and SPIR-V (`-spirv`), SPIRV-Cross or Metal Shader
Converter for Metal. Reflect bindings at build time to generate layouts.

## Leaky parts to plan for
- Descriptor models differ (D3D12 heaps vs Vulkan sets vs Metal argument buffers); design bindless
  first.
- Render passes: Vulkan/Metal tile-based mobile GPUs benefit from explicit load/store actions;
  expose them even if D3D12 ignores them.
- Memory allocation: Vulkan needs suballocation (VMA library; D3D12MA for D3D12).
- Feature tiers (mesh shaders, ray tracing, wave ops): capability queries with fallbacks.

## Verify
- Same frame rendered on each backend with image diff; validation layers (D3D12 debug layer, Vulkan
  validation) clean in CI; GPU-based validation runs nightly.
