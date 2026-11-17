---
id: creative-arts.animation.blender.hybrid-cpu-gpu-render
name: hybrid-cpu-gpu-render
category: creative-arts
field: animation
product: blender
tags: [blender, gpu, hybrid-cpu-gpu, cpu-gpu, cycles, render-optimization]
level: practitioner
status: docs-checked
description: "Decide when to add the CPU to a Cycles GPU render: how to enable it in preferences or CLI, the thread setting, how to measure the real gain, and when it can hurt."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/performance.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# hybrid-cpu-gpu-render

Goal: use the CPU and GPU together only when it actually lowers the frame time.

## Setup

Preferences > System > Cycles Render Devices > select the GPU backend (CUDA, OptiX, HIP, oneAPI or Metal), and **also tick the CPU** in the device list. Render Properties > Device: GPU Compute. Command line: append +CPU to the device, for example `-- --cycles-device OPTIX+CPU` (the manual: "Append +CPU to a GPU device to render on both CPU and GPU").

## Threads

Render Properties > Performance > Threads has **Threads Mode**: Auto-Detect (matches the number of logical processors) or Fixed. Fixed is useful when you want to keep using the computer while rendering, by setting a count below the number of logical processors. On the command line, `-t` / `--threads` sets the count (0 uses the system's processor count).

## When it may help

- A mid-range GPU with a strong many-core CPU, on scenes that fit in memory on both.

## When it may hurt

- A high-end GPU with a modest CPU: the CPU adds little and its coordination work can make the total no faster, or slower.
- Viewport rendering where the CPU is also busy with the interface or simulation.
- Render nodes that also run cache or simulation jobs.
- Path guiding is only available when rendering on a CPU and is not supported on any GPU, so do not rely on it for consistent results in a hybrid render.

## Measure

Render the same frame three ways (CPU only, GPU only, GPU+CPU) with fixed samples, and compare total render time, not per-sample time. Decide per machine type rather than per shot.

## Gotchas

- If adding the CPU slows the GPU, set Threads Mode to Fixed with one or two threads fewer than the logical processor count and re-measure.

## Verify

GPU+CPU total time is lower than GPU-only on a few sample frames from the shot. Otherwise untick the CPU.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST).
Confirmed: +CPU suffix on `--cycles-device`; `-t/--threads`; Threads Mode Auto-Detect/Fixed meaning; path guiding CPU-only and not on GPU.
Removed as unconfirmed: the claim that work is split in proportion to measured device speed, the 5 to 20 times CPU slowdown figure, the 16-core example, the 10 percent threshold, and the statement that Auto-detect starves the GPU driver thread.
Method: documentation only; no commands were run.
