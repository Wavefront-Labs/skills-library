---
id: computing-software.computer-graphics-engineering.gpu-optimisation.render-thread-architecture
name: render-thread-architecture
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, cpu-overhead, render-thread, multithreaded-rendering, job-system, command-recording, frame-pipelining, render-proxies]
level: advanced
status: draft
description: "Structure CPU rendering work: game/render thread split with frame-latched state, parallel command recording jobs, extraction of render proxies, and avoiding sync points."
sources: ["https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine", "https://docs.unrealengine.com/5.3/en-US/parallel-rendering-overview-for-unreal-engine/", "https://developer.nvidia.com/blog/vulkan-dos-donts/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render thread architecture

## 1. Pipeline of threads
A typical engine pipelines three stages across frames:
```
Frame N+2: Game/simulation thread (gameplay, physics, animation)
Frame N+1: Render thread (visibility, sorting, building draw lists, recording commands)
Frame N  : GPU executes
```
Each stage works on its own copy of the data it needs, so stages never wait on each other except at
frame boundaries. Unreal: Game thread -> Render thread -> RHI thread -> GPU.

## 2. Extraction (render proxies)
At the end of the game frame, **extract** a compact render representation (transforms, material
params, visibility flags) into a frame packet owned by the render thread. Game code never touches
render data directly (UE `FPrimitiveSceneProxy`, `ENQUEUE_RENDER_COMMAND`).
- Double/triple-buffer the packets; reuse allocations (linear frame allocators).

## 3. Parallel command recording
- Split the frame's passes or draw lists into chunks; record each on a worker with its own command
  allocator/pool (D3D12 `ID3D12CommandAllocator` per thread per frame, Vulkan `VkCommandPool` per
  thread per frame), then submit in order.
- Vulkan secondary command buffers or D3D12 bundles for reuse; most engines record primary lists in
  parallel and submit an ordered array.
- Visibility/culling as parallel jobs feeding sorted draw lists.

## 4. Avoid sync points
- No GPU readbacks in the frame (use N-frame-delayed results).
- No `Map` on resources in use by the GPU without ring buffers.
- Avoid blocking resource creation on the render thread; create on loader threads.
- Locks around shared caches (PSO, descriptor) cause contention: use per-thread caches and lock-free
  lookups.

## 5. Latency
Each pipelined stage adds a frame of input latency; reduce with Reflex-style just-in-time sampling,
or by overlapping game and render work within a frame (jobs) instead of fixed stage threads.

## Gotchas
- Shared mutable state between game and render threads leads to tearing/races: enforce ownership.
- Too many tiny jobs add overhead; target jobs of ~50-200 us.

## Verify
- [ ] CPU timeline shows render work spread across cores with no long waits.
- [ ] Game and render threads both under the frame budget; no per-frame readback stalls.
