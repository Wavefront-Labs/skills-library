---
id: computing-software.computer-graphics-engineering.gpu-optimisation.measuring-draw-call-cost
name: measuring-draw-call-cost
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, cpu-overhead, draw-call-cost, draw-calls, state-changes, driver-overhead, profiling, batching]
level: practitioner
status: draft
description: "Measure what a draw call really costs on the CPU: driver vs engine time, state-change classes, microbenchmarks per API, and deciding whether batching or API changes pay off."
sources: ["https://www.nvidia.com/docs/IO/8228/BatchBatchBatch.pdf", "https://gdcvault.com/play/1020791/Approaching-Zero-Driver-Overhead-in", "https://developer.arm.com/documentation/101897/latest/CPU-overheads/Draw-call-batching-best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring draw call cost

## 1. Where the time goes
Per draw, CPU time splits into:
- **Engine**: visibility, sorting, setting up constants, material/state lookup.
- **API/driver**: validation, state translation, descriptor/resource tracking, command encoding.
The classic "Batch, Batch, Batch" (Wloka 2003) result - a CPU-limited number of draws per second -
still applies conceptually; modern explicit APIs cut driver cost but engine cost remains.

## 2. Measure
- CPU profiler (Superluminal, VTune, Tracy, PIX timing) over the render thread: time inside
  driver DLLs (`nvwgf2umx.dll`, `amdxx64.dll`, `igd*`) vs engine code.
- Divide render-thread time by draw count for a per-draw cost (typical: 1-5 us in D3D11/GL per
  draw with state changes; well under 1 us for explicit APIs with prebuilt PSOs).
- Microbenchmark: loop N identical draws vs N draws with a PSO change vs texture change vs constant
  buffer change; per-API costs differ greatly.

## 3. State change cost classes (rough order, most to least expensive)
1. Render target / render pass changes.
2. Pipeline/program changes (shader switch).
3. Texture/descriptor set bindings.
4. Vertex/index buffer bindings.
5. Constant/uniform updates.
6. The draw itself.
Sort draws to minimise the expensive classes first.

## 4. Decide
- If render-thread time is far below frame budget, draw count isn't your problem; stop.
- If driver time dominates: reduce state changes, use instancing, multi-draw indirect, bindless.
- If engine time dominates: optimise culling/sorting/data layout or multithread recording.

## Gotchas
- GPU-side draw overhead also exists (tiny draws underutilise the GPU: each draw has setup cost of
  a few us of GPU front-end time); merge micro-draws even on explicit APIs.
- Debug builds and validation layers inflate per-draw cost 10x; measure release.

## Verify
- [ ] Per-draw CPU cost known for each target platform.
- [ ] Optimisation choice backed by driver vs engine time split.
