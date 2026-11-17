---
id: computing-software.computer-graphics-engineering.shader-programming.compute-image-filters-shared-memory
name: compute-image-filters-shared-memory
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, compute-blur, shared-memory-tiling, separable-blur, groupshared]
level: advanced
status: docs-checked
description: "Write fast compute-shader image filters: separable Gaussian blur with groupshared tiles plus apron, bank conflicts, and when a pixel shader is faster."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-attributes-numthreads", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#limits", "https://www.rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute image filters with shared memory tiles

## 1. Separable blur, horizontal pass
```hlsl
#define R 8                 // kernel radius
#define G 128               // threads per group along x
Texture2D<float4> Src; RWTexture2D<float4> Dst; static const float W[R+1] = { /* weights */ };
groupshared float4 tile[G + 2*R];
[numthreads(G,1,1)]
void BlurH(uint3 gid : SV_GroupID, uint3 tid : SV_GroupThreadID, uint3 dtid : SV_DispatchThreadID) {
  int2 p = int2(dtid.xy);
  tile[tid.x + R] = Src[clamp(p, 0, size - 1)];
  if (tid.x < R) {                                   // left and right apron
    tile[tid.x] = Src[clamp(p - int2(R, 0), 0, size - 1)];
    tile[tid.x + G + R] = Src[clamp(p + int2(G, 0), 0, size - 1)];
  }
  GroupMemoryBarrierWithGroupSync();
  float4 s = tile[tid.x + R] * W[0];
  [unroll] for (int i = 1; i <= R; i++) s += (tile[tid.x + R - i] + tile[tid.x + R + i]) * W[i];
  if (all(p < size)) Dst[p] = s;
}
```
Vertical pass identical with a column group (`numthreads(1,G,1)`) or transpose. Each texel is
read once from memory instead of 2R+1 times.

## 2. Tuning
- Store the tile as `half4` or a packed `uint` (RGBA8 / R11G11B10) to fit more in groupshared.
- Shared-memory budget: Vulkan guarantees only `maxComputeSharedMemorySize` of 16384 bytes (32768 in newer profiles); query it.
  Larger tiles can reduce occupancy.
- Check bank conflicts in a profiler; layout (float4 vs separate float arrays) can matter.

## 3. When a pixel shader wins
Small radii with bilinear-tap tricks (linear sampling reduces the tap count) in a fragment shader
may be as fast. Measure.

## Gotchas
- Missing barrier = reading uninitialised tile entries (flickering blocks).
- Image edges: clamp reads, and guard writes for partial groups.
- Very large radii: downsample first, or use a box-blur sliding window / Kawase blur.

## Verify
- [ ] Output matches a reference pixel-shader blur within 1e-3; profiler shows memory reads cut.

## Checked

Checked 2026-10-26 against Vulkan-Docs limits chapter (main, 2026-10-23), Microsoft numthreads page. Confirmed: `numthreads(X,Y,Z)` semantics and `SV_GroupThreadID`/`SV_DispatchThreadID`/`GroupMemoryBarrierWithGroupSync` usage in the HLSL example (apron loads and barrier ordering traced by hand); `maxComputeSharedMemorySize` minimum 16384 bytes (32768 in newer profiles). Removed as unconfirmed: the 32/64 KB groupshared budget, the bank-conflict float4 remark, the small-radius and tile-based-GPU claims (now hedged).

Method: documentation only; no commands were run.
