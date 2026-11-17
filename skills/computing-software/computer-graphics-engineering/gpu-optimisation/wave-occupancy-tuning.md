---
id: computing-software.computer-graphics-engineering.gpu-optimisation.wave-occupancy-tuning
name: wave-occupancy-tuning
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-memory-bandwidth, wave-occupancy, occupancy, vgpr, register-pressure, rdna, latency-hiding]
level: advanced
status: draft
description: "Tune wave/warp occupancy: register (VGPR) and shared-memory limits per SIMD, reading compiler stats, when higher occupancy helps or hurts, and wave32 vs wave64 on RDNA."
sources: ["https://gpuopen.com/learn/occupancy-explained/", "https://gpuopen.com/rga/", "https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#occupancy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wave occupancy tuning

## 1. What occupancy is
Number of waves (AMD) / warps (NVIDIA) resident per SIMD/SM relative to the maximum. More resident
waves let the scheduler hide memory latency by switching to another wave while one waits.

## 2. Limiters
- **Registers**: per-SIMD register file is shared; more VGPRs per thread = fewer waves.
  RDNA2 example (wave32): a SIMD's register file holds 1024 VGPRs per lane, and at most 16 waves
  fit, so 64 VGPRs -> 16 waves, 128 -> 8, 256 -> 4 (allocation granularity rounds up; see the
  tables in GPUOpen's "Occupancy explained"). RGA and RGP report VGPRs used and theoretical
  occupancy.
- **LDS / shared memory** per workgroup: big groupshared allocations limit concurrent groups.
- **Workgroup size** and wave slots; scalar registers (rarely).
NVIDIA: registers per thread (e.g. > 64 reduces occupancy), shared memory per block, block size;
CUDA occupancy calculator logic applies to compute in graphics APIs too.

## 3. Reading the numbers
- AMD: RGA (`rga -s vulkan --asic gfx1030 ...`) or RGP pipeline state: VGPR/SGPR/LDS usage and
  occupancy; RGP's wavefront occupancy timeline shows achieved occupancy per pass.
- NVIDIA: Nsight Graphics shader pipeline stats (registers, theoretical occupancy) and GPU Trace
  achieved occupancy with the limiting factor.
- Vulkan: `VK_KHR_pipeline_executable_properties` to query register counts at runtime.

## 4. When it matters
- Latency-bound shaders (many texture/memory fetches, low ALU between them) benefit from higher
  occupancy.
- ALU-bound shaders don't need high occupancy; forcing fewer registers may add spills (worse).
- Moderately low occupancy (4-8 waves) is fine if the shader has enough independent work
  (instruction-level parallelism).

## 5. Raising occupancy
- Reduce live variables across texture fetches; recompute cheap values instead of keeping them.
- Split uber-shaders so common paths don't pay for rare features' registers.
- Reduce groupshared size or tile size; use fp16 packed math (half the registers for some values).
- Avoid large local arrays (dynamically indexed arrays go to scratch or consume many VGPRs).
- RDNA: wave32 vs wave64 choice (driver decides for graphics; compute can hint via
  `[WaveSize(32)]` in SM 6.6).

## Gotchas
- Theoretical occupancy isn't achieved occupancy: small dispatches or barriers keep it low anyway.
- Higher occupancy can thrash caches (more waves competing); measure.

## Verify
- [ ] Register count and achieved occupancy recorded before/after changes.
- [ ] Pass time improved; not just occupancy number.
