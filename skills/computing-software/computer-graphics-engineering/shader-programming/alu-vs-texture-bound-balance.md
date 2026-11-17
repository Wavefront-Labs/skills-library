---
id: computing-software.computer-graphics-engineering.shader-programming.alu-vs-texture-bound-balance
name: alu-vs-texture-bound-balance
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-optimisation, alu-bound, texture-bound, lut, bandwidth-bound, shader-profiling]
level: advanced
status: draft
description: "Determine whether a shader is ALU-, texture- or bandwidth-bound and rebalance it: LUTs vs math, texture format and filtering costs, and unit counters."
sources: ["https://developer.arm.com/documentation/101897/latest/Fragment-shading", "https://developer.nvidia.com/blog/the-peak-performance-analysis-method-for-optimizing-any-gpu-workload/", "https://gpuopen.com/learn/rdna-performance-guide/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ALU vs texture-bound balance

## 1. Diagnose
- Hardware counters: NVIDIA Nsight "SOL" units (SM, TEX, L1, L2, DRAM throughput %) via the
  Peak-Performance-Percentage method; AMD RGP wavefront occupancy and instruction timing;
  Mali Streamline (arithmetic vs texture vs load/store cycles).
- Quick experiments: halve texture resolution or force a 1x1 mip (if faster: texture/bandwidth
  bound); remove half the math (if faster: ALU bound); halve render resolution (if no change:
  not pixel bound at all).

## 2. If texture bound
- Use compressed formats (BC/ASTC) and mipmaps; uncompressed RGBA8/RGBA16F thrash cache.
- Trilinear and anisotropic cost more per sample (aniso 16x can be multiple samples); limit
  anisotropy on low-importance textures.
- Pack channels (ORM: occlusion/roughness/metal in one texture) to cut fetches.
- 3D/volume and cube samples cost more than 2D on some hardware.

## 3. If ALU bound
- Replace expensive functions with LUT textures only when the texture unit has headroom
  (e.g. BRDF split-sum LUT, complex curves). Otherwise approximations: fast `acos`,
  `rsqrt` instead of `1/sqrt`, polynomial fits.
- fp16 on mobile and AMD (packed math).
- Move per-pixel work to per-vertex or to lower-resolution passes.

## 4. Balance rule
Units run in parallel: a shader with both moderate ALU and texture use is limited by the
busier unit. Trading one for the other only helps if the other has headroom.

## Gotchas
- "Texture bound" can really be memory bandwidth (cache misses): check L2/DRAM, not TEX units.
- LUTs in high-precision formats (RGBA32F) can be slower than the math they replace.

## Verify
- [ ] After the change, the limiting unit's throughput falls and frame time improves.
