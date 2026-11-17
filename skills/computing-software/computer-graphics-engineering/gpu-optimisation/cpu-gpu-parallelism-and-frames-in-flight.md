---
id: computing-software.computer-graphics-engineering.gpu-optimisation.cpu-gpu-parallelism-and-frames-in-flight
name: cpu-gpu-parallelism-and-frames-in-flight
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, frame-pacing, cpu-gpu-parallelism, frames-in-flight, gpu-stalls, readback-latency, pipelining]
level: sme
status: draft
description: "Keep CPU and GPU busy in parallel: frames-in-flight pipelining, per-frame resource rings, avoiding sync stalls and readbacks, and reading timelines to find bubbles."
sources: ["https://vkguide.dev/docs/new_chapter_1/vulkan_mainloop_code/", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/user-mode-heap-synchronization", "https://developer.nvidia.com/blog/advanced-api-performance-cpus/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CPU/GPU parallelism and pipelining

## 1. Model
CPU records frame N+1 while the GPU executes frame N. Any point where one waits for the other is a bubble.
Frame time ~ max(CPU, GPU) only if they overlap; otherwise CPU + GPU.

## 2. Frames in flight
- 2 (sometimes 3) frames in flight: per-frame copies of command allocators/pools, constant/upload ring
  segments, descriptor pools.
- At frame start, wait for the fence of frame `N - framesInFlight` only, then reuse its resources.
```cpp
uint32_t f = frameIndex % kFramesInFlight;
vkWaitForFences(dev, 1, &frames[f].fence, VK_TRUE, UINT64_MAX);
vkResetFences(dev, 1, &frames[f].fence);
vkResetCommandPool(dev, frames[f].pool, 0);
// record, submit with frames[f].fence
```
D3D12: one fence value per frame slot, `SetEventOnCompletion` + wait only if `GetCompletedValue() < value`.
- More frames in flight = more input latency; 2 is the usual balance, and latency tools (Reflex, Anti-Lag)
  limit the queue further.

## 3. Common stalls
- **Readback** of GPU results the same frame (`glReadPixels`, `glGetQueryObject` without availability check,
  mapping a buffer the GPU still uses): read N-2 frames later via a ring of readback buffers and fences.
- **Updating a resource in use**: GL `glBufferSubData` on a buffer the GPU reads forces sync; orphan or
  persistent-map with fences. D3D11 `Map(WRITE)` without DISCARD/NO_OVERWRITE.
- **WaitIdle** calls (`vkDeviceWaitIdle`, `vkQueueWaitIdle`, flush-and-wait in D3D12) in the frame loop.
- **Present blocking** with FIFO when the queue is full: CPU appears slow but is waiting on vsync.
- Shader compilation or pipeline creation on the render thread.

## 4. Find bubbles
- GPU timeline gaps between submissions: PIX timing captures, Nsight Systems (CPU threads + GPU queue on one
  timeline), RGP, Perfetto GPU tracks on Android.
- CPU samples inside driver wait functions (`WaitForSingleObject`, `vkWaitForFences`) = GPU-bound or a sync
  point; GPU idle while CPU records = CPU-bound.
- Submit work in a few chunks per frame rather than one at the end, so the GPU starts earlier.

## Gotchas
- Per-frame resources indexed by swapchain image index instead of frame-in-flight index cause races or
  over-allocation (they are different counts).
- Timer queries also need N-2 readback.

## Verify
- [ ] Nsight Systems/PIX timeline: GPU queue continuously busy when GPU-bound; no wait calls on the render
  thread besides the frame-slot fence; frame time ~ max(CPU, GPU).
