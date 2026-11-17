---
id: computing-software.computer-graphics-engineering.gpu-optimisation.gpu-hardware-counters-top-down-analysis
name: gpu-hardware-counters-top-down-analysis
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, gpu-counters, top-down-analysis, speed-of-light, occupancy, nsight-gpu-trace, radeon-gpu-profiler]
level: advanced
status: draft
description: "Use GPU hardware counters for top-down bottleneck analysis: unit throughputs (SOL), occupancy, cache hit rates, stall reasons, and mapping counters to concrete fixes."
sources: ["https://developer.nvidia.com/blog/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/", "https://gpuopen.com/rgp/", "https://developer.arm.com/documentation/102478/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware counters and top-down analysis

## 1. Peak-performance-percentage method (NVIDIA)
For a pass/draw, read each unit's throughput as a percentage of its peak ("SOL%"): SM (shader),
L1/TEX, L2, VRAM, raster/ROP/ZROP, VAF (vertex attribute fetch), PD/primitive distributor, etc.
- **Top unit SOL% > ~70-80%**: that unit is the limiter; reduce work for it.
- **All units low**: latency-bound or underutilised: low occupancy, insufficient parallelism
  (small dispatches), stalls on dependencies or synchronisation.
Nsight Graphics GPU Trace presents this as a throughput table with "top units".

## 2. Common counters and what they mean
| Counter | High value means | Fixes |
|---|---|---|
| SM throughput / ALU busy | math-bound | cheaper math, fp16, fewer instructions |
| TEX / L1 throughput, texture stalls | texture-bound | fewer fetches, compressed formats, lower aniso, mip bias |
| L2 / VRAM bandwidth | memory-bound | smaller formats, better locality, compression (DCC), fewer passes |
| ROP / CROP | blending/output-bound | fewer/lighter targets, less overdraw, avoid wide formats |
| ZROP / depth | depth-bound | depth prepass trade-off, less overdraw of depth-only |
| VAF / IA | vertex fetch-bound | quantised attributes, vertex cache optimisation |
| Warp occupancy low + stalls "long scoreboard" | memory latency not hidden | reduce registers/shared memory to raise occupancy, prefetch |

## 3. AMD (RGP) and others
- Radeon GPU Profiler: wavefront occupancy timeline, per-event duration, instruction timing
  (hotspots with latency), cache counters via the counters view; RGA for VGPR counts.
- Arm Streamline (Mali): fragment/non-fragment active cycles, shader core utilisation by pipe
  (arithmetic, load/store, texture, varying), external read/write bandwidth.
- Qualcomm Snapdragon Profiler and Apple Xcode GPU counters (limiter/utilisation per unit) work the
  same way: find the limiter first.

## 4. Process
1. Pick the most expensive pass from timing.
2. Read limiter counters for that pass.
3. Apply one fix aimed at that unit; re-measure (the limiter may move).

## Gotchas
- Counters are per pass/range; averaging over the whole frame hides limiters.
- Profiling with clocks unlocked gives noisy numbers; lock clocks (Nsight "lock to base", `nvidia-smi
  -lgc`, AMD stable power state `SetStablePowerState` in D3D12).

## Verify
- [ ] Each optimisation is justified by a counter that moved.
- [ ] Before/after captures saved with locked clocks.
