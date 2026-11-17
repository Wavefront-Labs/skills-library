---
id: computing-software.computer-graphics-engineering.rendering-techniques.wavefront-path-tracing-on-gpus
name: wavefront-path-tracing-on-gpus
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, ray-tracing, wavefront-path-tracing, gpu-path-tracing, megakernel, work-queues, ray-sorting, cuda]
level: sme
status: docs-checked
description: "Structure a GPU path tracer as a wavefront with work queues instead of a megakernel: why divergence and register pressure hurt, and what pbrt-v4 requires of a GPU."
sources: ["https://research.nvidia.com/publication/2013-07_megakernels-considered-harmful-wavefront-path-tracing-gpus", "https://pbr-book.org/4ed/Wavefront_Rendering_on_GPUs", "https://github.com/mmp/pbrt-v4"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wavefront path tracing on GPUs

## 1. Megakernel problem
Porting a large CPU path tracer into one equally large GPU kernel (a megakernel) is generally not a
good approach (Laine, Karras, Aila, HPG 2013, "Megakernels Considered Harmful"). Two costs:
- Divergence in control flow carries a substantial penalty under the GPU's SIMT execution model.
- High register usage lessens the latency-hiding capability the GPU's high-latency, high-bandwidth
  memory system depends on.
Both are worst when materials are expensive to evaluate. The paper's wavefront formulation is much
better suited than the megakernel when several complex materials are present in the scene.

## 2. Wavefront architecture
Process many rays simultaneously, with rendering work organised in queues that collect related tasks
so they are processed together (PBR 4th ed., chapter 15). Design questions to answer for your own
renderer: which stages exist (ray generation, intersection, shading, shadow rays), what each queue
holds, and how per-path state is laid out in memory. Data layout and parallelism, not new rendering
algorithms, decide GPU performance; implementation-level choices can change it by orders of magnitude.

## 3. pbrt-v4 as a reference
- pbrt's GPU path is `WavefrontPathIntegrator`, a volumetric path tracer; it reuses the same classes
  and functions as the CPU `VolPathIntegrator`.
- It needs a unified address space shared by CPU and GPU, a C++17-capable GPU toolchain, and GPU ray
  intersection (hardware or vendor software).
- At the time of writing only NVIDIA CUDA/OptiX met all three. The README asks for CUDA 11.0 or later
  and OptiX 7.1 or later, and the GPU is used only when `--gpu` is given.
- The book's example scene rendered about 37 times faster on a 2020-era high-end GPU than on an
  8-core CPU (318.6 s vs 11,983 s at 2048 samples per pixel). Treat as one data point, not a rule.
- The wavefront layout is usually a poor fit for CPUs: pbrt's `--wavefront` option on the CPU is for
  debugging, and performance is almost always worse than `VolPathIntegrator`.

## Gotchas
- Wavefront is not automatically faster. Compare against a megakernel on your own scenes and
  materials; the published advantage is for scenes with multiple expensive materials.
- Read the pbrt-v4 `gpu/` directory and the book chapter for queue and path-state details rather than
  guessing them.

## Checked
2026-11-08. Confirmed against the NVIDIA Research publication page (abstract), PBR 4th edition chapter 15 intro and the pbrt-v4 README: divergence and register-pressure argument, queue-based organisation, `WavefrontPathIntegrator`, its three platform requirements, CUDA/OptiX versions, `--gpu`, the CPU `--wavefront` caveat and the 37x example. Removed: named queue types, the stage-by-stage kernel list, the megakernel vs wavefront trade-off table, Shader Execution Reordering, queue and sorting tips (none stated in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Wavefront and megakernel versions converge to the same image.
- [ ] Profiler shows higher SIMD efficiency per material kernel.
