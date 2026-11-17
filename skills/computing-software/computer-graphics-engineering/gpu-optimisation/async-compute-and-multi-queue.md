---
id: computing-software.computer-graphics-engineering.gpu-optimisation.async-compute-and-multi-queue
name: async-compute-and-multi-queue
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [gpu-optimisation, async-compute, multi-queue, compute-queue, copy-queue, queue-synchronization, overlap, fine-grained-preemption, d3d12, vulkan, fences, timeline-semaphores]
level: advanced
status: draft
description: "Overlap graphics and compute work on separate GPU queues for real gains: when async compute helps vs hurts, cross-queue synchronization, and vendor scheduling differences."
sources: ["https://developer.nvidia.com/dx12-dos-and-donts", "https://gpuopen.com/learn/concurrent-execution-asynchronous-queues/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Async compute and multi-queue GPU work

**Goal:** fill GPU idle time (e.g. graphics queue bottlenecked on fixed-function
work while ALUs sit idle) with compute work on a separate queue — correctly
synchronised, and only where it's actually a win.

## Why it exists
A GPU frame often bottlenecks on a specific unit: ROP/fixed-function during a
shadow pass, or memory bandwidth during a geometry-heavy pass, while shader ALUs
are underused. **Async compute** submits independent compute work (post-processing
prep, culling, particle sim, SSAO) on a separate hardware queue so the scheduler
can interleave it into those idle slots — a real throughput gain, not just
API-level parallelism.

## Queue types
- **Graphics queue**: handles draw calls and graphics pipeline work; most engines
  run their main pass here.
- **Compute queue**: dispatch-only, no graphics pipeline state — for compute
  shaders that don't need the rasteriser.
- **Copy queue**: dedicated to DMA transfers (uploads, resource copies) — frees the
  graphics/compute queues from being blocked on data movement.
- Hardware support for genuinely concurrent execution across queues (not just API
  exposure of multiple queues) varies by vendor/architecture — profile on your
  actual target hardware, don't assume async compute helps uniformly across
  NVIDIA/AMD/Intel/mobile GPUs.

## Synchronisation across queues
- D3D12: `ID3D12Fence` signalled from one queue, waited on from another
  (`Wait`/`Signal` on the queue, not the command list) — this is the only legal
  cross-queue dependency mechanism; a resource barrier alone does not synchronise
  across queues.
- Vulkan: **timeline semaphores** (preferred over binary semaphores for cross-queue
  deps with multiple in-flight frames) — `vkQueueSubmit` wait/signal on a
  monotonically increasing value, avoids the semaphore-reuse hazards binary
  semaphores have.
- Resources touched by both queues (e.g. a UAV written by compute, read by
  graphics) still need the usual state-transition/UAV barrier — on whichever queue
  does the state change — plus the queue-level fence to order the *timing*, since
  barriers alone don't cross queue boundaries.

## When it helps vs hurts
- Helps: independent work with no data dependency on the current frame's graphics
  pass (particle simulation for next frame, culling for next frame, post-process
  LUT generation), scheduled to overlap a graphics-bound stretch.
- Hurts: if the compute work actually contends for the **same bottleneck**
  resource (e.g. compute work is also bandwidth-heavy during a bandwidth-bound
  graphics pass) — no idle capacity exists to fill, and you've just added
  synchronisation overhead for no overlap.
- Hurts: naive overlap where the compute work has a data dependency on the current
  frame's graphics output — forces a sync point that serialises the queues anyway,
  losing the benefit while keeping the complexity.
- Console/fixed-hardware targets (where async compute was popularised, e.g. PS4/
  Xbox One era) see more reliable, measurable wins than PC, where driver/scheduler
  behaviour varies more.

## Verify
- [ ] GPU timeline capture (PIX, RGP, Nsight) shows the compute queue work
      actually overlapping graphics queue idle time, not serialising after it.
- [ ] Cross-queue resource access has both a queue-level fence/semaphore AND the
      usual state/UAV barrier — not one substituting for the other.
- [ ] Measured frame time improvement on real target hardware, not just "the API
      allows it" — re-test if moving to different GPU vendors/generations.
- [ ] Compute work scheduled genuinely independent of the current frame's
      in-flight graphics output (no implicit serialising dependency).
