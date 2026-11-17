---
id: computing-software.computer-graphics-engineering.gpu-optimisation.performance-regression-testing
name: performance-regression-testing
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, performance-regression, benchmarking, ci, timestamp-queries, statistics, performance-testing]
level: advanced
status: draft
description: "Catch rendering performance regressions automatically: deterministic benchmark scenes, locked clocks, GPU timestamp collection, statistical thresholds and CI dashboards."
sources: ["https://docs.unrealengine.com/5.3/en-US/performance-and-profiling-in-unreal-engine/", "https://learn.microsoft.com/en-us/windows/win32/api/d3d12/nf-d3d12-id3d12device-setstablepowerstate", "https://developer.nvidia.com/blog/advanced-api-performance-setstablepowerstate/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance regression testing

## 1. Deterministic workloads
- Fixed camera paths (flythroughs) or fixed viewpoints in representative levels; fixed time step,
  random seeds and simulation state; disable dynamic resolution and adaptive quality.
- Warm up: skip the first N frames (shader compilation, streaming), or pre-load everything.

## 2. Stable measurements
- Lock GPU clocks: D3D12 `ID3D12Device::SetStablePowerState(TRUE)` (developer mode only),
  `nvidia-smi -lgc <base>,<base>`, AMD Radeon Developer Panel "stable clocks"; on mobile, use
  devices with performance-mode APIs and control thermals (cool-down between runs).
- Disable vsync, overlays, background apps; same driver version per baseline.
- Collect per-pass GPU timestamps (queries around each pass) and CPU scopes, not just frame time.

## 3. Statistics
- Run each test multiple times; use median and percentiles (p95/p99 frame time) rather than mean.
- Regression threshold relative to noise: e.g. flag if median increases more than max(3%, 3 x MAD
  of the baseline runs).
- Compare against a rolling baseline from main, not a fixed old number.

## 4. CI integration
- Nightly (or per merge) runs on dedicated hardware per platform tier.
- Store results in a time-series DB/dashboard (per test, per pass); auto-bisect regressions between
  commits using the same harness.
- Also track memory (VRAM, texture pool), draw calls, triangle counts and PSO compile counts -
  cheaper to measure and often the cause.

## 5. Unreal/Unity hooks
- Unreal: `-benchmark -fps=30 -deterministic`, Gauntlet automation, `stat unit`/CSV profiler
  (`-csvprofile`) output parsed by CI.
- Unity: Performance Testing package (`Measure.Frames()`), Profiler recorders for markers.

## Gotchas
- Thermal throttling makes later runs slower; interleave A/B runs.
- Shader cache state differs between runs; clear or pre-warm consistently.

## Verify
- [ ] Repeated identical runs vary by less than the alert threshold.
- [ ] A deliberately injected regression is detected and bisected.
