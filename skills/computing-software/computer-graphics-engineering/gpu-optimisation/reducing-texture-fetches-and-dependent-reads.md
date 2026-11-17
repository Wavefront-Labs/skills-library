---
id: computing-software.computer-graphics-engineering.gpu-optimisation.reducing-texture-fetches-and-dependent-reads
name: reducing-texture-fetches-and-dependent-reads
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, shader-optimisation, dependent-texture-reads, texture-fetch, channel-packing, texture-gather, texture-bound]
level: practitioner
status: draft
description: "Reduce texture fetch cost: pack channels, avoid dependent texture reads on mobile, use gather and mip/LOD choices, and share samples across neighbouring pixels."
sources: ["https://developer.arm.com/documentation/101897/latest/Shader-code/Texture-sampling-performance", "https://developer.apple.com/documentation/metal/resource_fundamentals/optimizing_texture_data", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/gather--direct3d-10-1-"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reducing texture fetches and dependent reads

## 1. Count and pack
- Pack scalar maps into one texture: ORM (occlusion, roughness, metallic) in RGB, height in A.
- Normal maps: store XY only (BC5) and reconstruct Z.
- Texture arrays and atlases reduce binding changes but not fetch count.

## 2. Dependent texture reads
A dependent read uses coordinates computed from another fetch or from non-trivial math in the
fragment shader. Older and mobile GPUs (PowerVR SGX era, some Mali/Adreno) prefetch texels for
coordinates that come straight from varyings; dependent reads stall until the first fetch returns.
- Pass final UVs from the vertex shader (scrolling, tiling) when possible.
- Chains (noise texture -> UV offset -> texture) serialise latency; keep them short.
On modern desktop GPUs latency hiding through occupancy makes this matter less, but long fetch
chains still increase register pressure.

## 3. Fetch fewer texels
- `textureGather` / `GatherRed` returns 4 texels of one channel in one instruction: ideal for PCF
  shadows, depth-aware upsampling, SSAO.
- Bilinear "free" taps: place samples between texels to average 2-4 texels per fetch (separable
  blur trick).
- Use lower mips for blurry lookups (`textureLod` with a bias) - fewer cache misses.
- Anisotropic 16x on everything costs bandwidth; use 4-8x for most, 16x only for ground.

## 4. Share work across pixels
- Compute shaders: load a tile plus apron into shared memory once; each thread reads neighbours from
  shared memory (blur, SSAO, bilateral filters).
- Quad intrinsics (`QuadReadAcrossX`, `subgroupQuadSwapHorizontal`) share values among the 2x2 quad
  without fetches.

## 5. Format and filtering
Fetch cost depends on format: RGBA32F is 2-4x the cost of RGBA8 on many GPUs; trilinear and
anisotropic filters take extra cycles. Use BCn/ASTC compressed formats (also smaller in cache).

## Gotchas
- Sampling sRGB textures as linear (or the reverse) is a correctness bug, not a perf trick.
- Branching around fetches in non-uniform control flow breaks derivatives; use `textureGrad` or
  compute derivatives before the branch.

## Verify
- [ ] Profiler texture-unit utilisation and L1/L2 hit rate improve.
- [ ] Fetch count per shader (offline compiler) reduced.
