---
id: computing-software.computer-graphics-engineering.gpu-optimisation.gpu-memory-bandwidth-and-occupancy
name: gpu-memory-bandwidth-and-occupancy
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [gpu-optimisation, occupancy, memory-bandwidth, register-pressure, warp, wavefront, cache-hit-rate, bank-conflicts, coalesced-access, texture-cache, roofline-model, shared-memory, latency-hiding]
level: advanced
status: draft
description: "Diagnose GPU occupancy and bandwidth problems: warp occupancy limiters (registers, shared memory), memory coalescing, cache behaviour, and the roofline model."
sources: ["https://developer.nvidia.com/blog/cuda-pro-tip-occupancy-api-simplifies-launch-configuration/", "https://docs.nvidia.com/nsight-compute/ProfilingGuide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU memory bandwidth and occupancy

**Goal:** know whether a kernel/shader is compute-bound, bandwidth-bound or
latency-bound before changing anything — optimising the wrong one wastes time and
sometimes makes things worse. Builds on
`computer-graphics-engineering.gpu-optimisation.gpu-profiling-and-bottleneck-diagnosis`.

## Occupancy: why it matters
GPUs hide memory latency by having many warps/wavefronts (groups of 32/64 threads)
resident per SM/CU and switching between them while one waits on memory. **Low
occupancy = not enough resident warps to hide latency = stalls visible as idle
compute**. Occupancy is capped by whichever resource runs out first:
- **Registers per thread**: a kernel using too many registers per thread reduces
  how many warps fit per SM simultaneously. Check with `--ptxas-options=-v` (CUDA)
  or the compiler's resource usage report; cap with `maxrregcount` /
  `__launch_bounds__` if a kernel is register-bound and could trade a little
  per-thread speed for more parallelism.
- **Shared memory per block**: same trade-off — a block requesting more shared
  memory than needed limits how many blocks run concurrently per SM.
- **Thread/block limits**: hardware caps threads per SM and blocks per SM
  independently; a block size that doesn't divide evenly can waste slots.
- High occupancy is necessary but not sufficient for speed — a kernel can have
  100% occupancy and still be bandwidth-bound; occupancy is a hiding-latency
  lever, not a correctness or ceiling metric by itself.

## Memory coalescing and bank conflicts
- **Coalesced global memory access**: when consecutive threads in a warp access
  consecutive memory addresses, the hardware services them in one (or few) memory
  transactions. Strided or scattered access (e.g. column-major access on a
  row-major buffer) multiplies transaction count — same data volume, far more
  bandwidth consumed.
- **Shared memory bank conflicts**: shared memory is divided into banks (commonly
  32); if multiple threads in a warp hit the same bank on different addresses
  simultaneously, accesses serialise. Padding array strides (`+1` element) to
  avoid power-of-two strides matching the bank count is the classic fix.
- **Texture/L1/L2 cache**: textures are cached with 2D locality in mind
  (swizzled/tiled layout) — sampling in raster order across a large texture is
  cache-friendlier than random access; this is why texture fetches, not raw buffer
  reads, are preferred for image-like data with spatial locality.

## Roofline model: compute-bound vs bandwidth-bound
Plot achieved FLOPs/sec against arithmetic intensity (FLOPs per byte moved from
memory). The hardware's two ceilings — peak compute throughput and peak memory
bandwidth — intersect at a knee:
- Left of the knee (low arithmetic intensity): **bandwidth-bound** — adding more
  compute does nothing; the fix is fewer bytes moved (compression, better layout,
  fusing kernels to avoid round-tripping through memory) or better coalescing.
- Right of the knee: **compute-bound** — the fix is fewer instructions/better ALU
  utilisation, not memory access patterns.
- Nsight Compute / RGP report this directly (a roofline chart or an equivalent
  "memory vs compute throughput %" pair) — read it before guessing which lever to pull.

## Gotchas
- Occupancy calculators give a theoretical maximum; actual achieved occupancy
  (measured, via profiler) is often lower due to tail effects (last wave of blocks
  not filling the GPU) and uneven work distribution.
- Increasing occupancy by cutting shared memory usage can increase global memory
  traffic (less data reuse) — a net loss if the kernel was bandwidth-bound to begin with.
- Fusing kernels to avoid writing an intermediate result to memory and reading it
  back is one of the highest-value bandwidth optimisations and is invisible to
  per-kernel occupancy metrics.

## Verify
- [ ] Profiler's memory throughput % and compute throughput % checked to classify
      the kernel (roofline position) before changing code.
- [ ] Measured (not just theoretical) occupancy checked via profiler, not just the
      launch-config calculator.
- [ ] Global memory access pattern checked for coalescing on the hot path, not
      just shared memory.
- [ ] Any shared-memory-reduction change re-measured for a net memory-traffic
      increase, not assumed to be a pure win.
