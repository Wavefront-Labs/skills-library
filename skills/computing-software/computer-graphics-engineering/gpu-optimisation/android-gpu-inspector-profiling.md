---
id: computing-software.computer-graphics-engineering.gpu-optimisation.android-gpu-inspector-profiling
name: android-gpu-inspector-profiling
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, tile-based-gpus, android-gpu-inspector, agi, android, vulkan, perfetto, mobile-profiling]
level: practitioner
status: draft
description: "Profile Android graphics with Android GPU Inspector: system profiles with GPU counters and timelines, Vulkan frame profiler captures, and reading results."
sources: ["https://developer.android.com/agi", "https://gpuinspector.dev/docs/", "https://perfetto.dev/docs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android GPU Inspector (AGI)

## 1. Setup
- Install AGI on the host; device must be on the supported list (recent Pixel, Samsung Galaxy with
  Adreno/Mali, etc.) with a compatible driver; enable developer options and USB debugging.
- The app must be **debuggable** (`android:debuggable="true"`) or the device rooted, for API
  interception (frame profiling).

## 2. System profile
Record a trace (built on Perfetto) of a few seconds:
- **GPU counters**: GPU utilisation, frequency, shader ALU/texture busy, vertex/fragment
  workload, memory read/write bandwidth (vendor-specific counter sets for Adreno and Mali).
- **GPU queue/render stage timelines**: per render pass (binning/rendering phases on Adreno
  show as separate stages), surface flinger and display composition.
- **CPU scheduling**: thread states per core, frequency, your app's threads with ATrace markers
  (`ATrace_beginSection` / `Trace.beginSection`).
- **Vulkan/GLES API events** (with layers enabled).
Use it to classify CPU vs GPU bound and find frame pacing problems (late present, SurfaceFlinger
misses).

## 3. Frame profiler
Captures a single Vulkan frame (GLES support is limited): per-render-pass and per-draw GPU timing,
render pass attachment load/store ops, framebuffer views, shader views, and resource state.
Ideal for finding unnecessary loads/stores, oversized passes and expensive draws on real mobile
hardware.

## 4. Typical findings
- Render passes with LOAD/STORE where DONT_CARE suffices (bandwidth).
- Too many render passes (pass breaks from mid-frame reads).
- GPU frequency ramping (thermal) causing variable frame time.
- CPU main thread blocking on `vkAcquireNextImageKHR` or fences.

## 5. Complementary tools
Arm Performance Studio (Streamline, Frame Advisor) for Mali, Snapdragon Profiler for Adreno,
Android Studio's Perfetto UI for system traces.

## Gotchas
- Counter availability varies by driver; update the device OS.
- Profiling overhead with API interception changes timings; use system profiles for timing.

## Verify
- [ ] System profile shows per-pass GPU stages and bandwidth for your game.
- [ ] Frame profiler capture reviewed for load/store ops on every pass.
