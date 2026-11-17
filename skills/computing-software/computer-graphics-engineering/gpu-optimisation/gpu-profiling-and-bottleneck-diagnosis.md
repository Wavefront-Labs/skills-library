---
id: computing-software.computer-graphics-engineering.gpu-optimisation.gpu-profiling-and-bottleneck-diagnosis
name: gpu-profiling-and-bottleneck-diagnosis
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [gpu-optimisation, gpu-optimization, gpu-profiling, bottleneck, cpu-bound, gpu-bound, draw-calls, batching, instancing, overdraw, fill-rate, memory-bandwidth, vertex-bound, occupancy, timestamp-queries, nsight-graphics, radeon-gpu-profiler, pix, renderdoc, xcode-gpu-frame-capture, arm-mobile-studio, snapdragon-profiler, tile-based-rendering, frame-budget]
level: advanced
status: draft
description: "Find and fix what limits frame time: CPU- vs GPU-bound tests, per-pass GPU timestamps, resolution/overdraw/bandwidth experiments, draw-call batching, and tool choice per vendor."
sources: ["https://developer.nvidia.com/nsight-graphics", "https://gpuopen.com/rgp/", "https://developer.arm.com/documentation/101897/latest/", "https://devblogs.microsoft.com/pix/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU profiling and bottleneck diagnosis

**Goal:** know *why* a frame is slow before changing anything — then apply the fix that
matches the bottleneck. Optimising the wrong stage is the most common waste of time in
graphics work.

## 0. Measure the right thing
- Use **milliseconds per frame**, never fps, for comparisons (60→50 fps is +3.3 ms;
  200→150 is +1.7 ms). Budgets: 16.67 ms @60, 11.1 @90 (VR), 8.33 @120.
- Profile **release builds on target hardware** at the target resolution, with vsync off
  (or measure GPU time directly), thermals settled (mobile throttles after minutes).
- Capture a representative worst-case scene, not the menu.

## 1. CPU-bound or GPU-bound?
- Compare CPU frame time (main + render thread) with GPU frame time (timestamp queries or
  the engine's `stat unit`/profiler GPU line). The larger one is the bottleneck.
- Quick experiments:
  - **Drop render resolution to ~25% of pixels.** Frame time falls a lot → pixel-bound
    (fragment shading, fill rate, bandwidth). Barely changes → CPU or vertex/geometry bound.
  - **Skip submitting draws** (or freeze the simulation) → if it's still slow, it's not rendering.
- GPU idle gaps in a timeline (Nsight Systems, PIX timing, RGP) with a busy CPU = CPU-bound:
  too many draw calls/state changes, or the CPU waits on a GPU readback (sync stalls).

## 2. Per-pass GPU timing
Wrap each pass (shadows, G-buffer, lighting, transparency, post, UI) in **GPU timestamp
queries** (`vkCmdWriteTimestamp2`, D3D12 `EndQuery` with timestamp heap, GL
`glQueryCounter`) and keep them in a debug overlay. Read results a few frames late to
avoid stalling. This tells you which pass to open in a frame debugger.

## 3. Inside a GPU-bound pass — the usual suspects
| Symptom / experiment | Likely limiter | Fixes |
|---|---|---|
| Cost scales with resolution; simple shader | Fill rate / **overdraw** / ROP | Front-to-back opaque sort, depth pre-pass for expensive shaders, reduce transparent layers and particle size, smaller render targets (half-res effects). |
| Cost scales with resolution; heavy shader | **Fragment ALU** | Simplify math, move work to vertex stage or precompute into textures/LUTs, use half precision on mobile, variable rate shading. |
| Texture-heavy pass, profiler shows high memory throughput | **Bandwidth** | Compressed textures (BC/ASTC), mipmaps (always), smaller G-buffer formats (e.g. RGBA8/R11G11B10 instead of RGBA16F where precision allows), fewer full-screen passes, on tile GPUs avoid unnecessary loads/stores. |
| Cost scales with triangle count, not resolution | **Vertex / primitive** | LODs, culling (frustum, occlusion, backface), meshlet/mesh-shader pipelines, avoid micro-triangles (<~4 px each wastes quad shading). |
| Low occupancy in profiler, long-latency stalls | **Register pressure** | Reduce live variables, split shaders, check compiler output (RGA, Nsight shader profiler). |
| Compute pass with poor throughput | Divergence / memory access | Coherent access patterns, shared memory tiling, workgroup size multiple of 32/64. |
Hardware counters in vendor tools (NVIDIA's "throughput" metrics, AMD RGP wave occupancy,
Arm/Qualcomm counters) confirm which unit is saturated — use them rather than guessing.

## 4. CPU-side rendering cost
- Draw calls: each has CPU (and driver) overhead. Rough guide: low thousands per frame is
  fine on modern desktop APIs, a few hundred is a safe mobile ceiling — profile, these vary.
- Reduce with: **instancing**, merging static geometry, texture atlases/arrays so more
  objects share a material, bindless resources, GPU-driven rendering (indirect draws with
  GPU culling).
- Sort draws by state (pipeline/PSO → material → mesh) to cut state changes.
- Never read back GPU results (queries, buffers) in the same frame; that serialises CPU and GPU.

## 5. Tool choice
- Cross-vendor frame debugger: **RenderDoc** (correctness, per-draw inspection; timings
  are indicative only).
- NVIDIA: **Nsight Graphics** (GPU Trace for unit throughput), Nsight Systems (CPU/GPU timeline).
- AMD: **Radeon GPU Profiler** (RGP), Radeon GPU Analyzer for shader ISA.
- Windows D3D12: **PIX** timing + GPU captures. Apple: Xcode Metal frame capture & counters.
- Mobile: Arm Performance Studio (Streamline), Snapdragon Profiler, Android GPU Inspector.

## Gotchas
- Driver/OS overlays, recording software and debug layers change timings — disable them.
- An improvement within noise isn't one: average over hundreds of frames, compare
  distributions (p50/p95/p99), and change one thing at a time.
- Tile-based mobile GPUs punish full-screen passes and render-target switches far more
  than desktop GPUs; desktop-derived intuitions mislead.

## Verify
- [ ] Bottleneck classified (CPU / GPU pass / unit) with a measurement, before any fix.
- [ ] Per-pass GPU timings visible in a debug overlay.
- [ ] Each optimisation shows a before/after ms delta beyond run-to-run noise.
- [ ] p95/p99 frame times (hitches) checked, not just the average.
- [ ] Results reproduced on the lowest-spec target device.
