---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-radix-and-bitonic-sort
name: gpu-radix-and-bitonic-sort
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, gpu-radix-sort, bitonic-sort, prefix-sum, onesweep]
level: sme
status: draft
description: "Sort keys on the GPU with compute shaders: bitonic sort for small fixed sizes, LSD radix sort with prefix sums for large arrays, and vendor libraries."
sources: ["https://gpuopen.com/fidelityfx-parallel-sort/", "https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda", "https://research.nvidia.com/publication/2022-06_onesweep-faster-least-significant-digit-radix-sort-gpus"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU sorting: bitonic and radix

Uses: particle/splat depth sorting for transparency, Morton-code sorting for BVH/LBVH builds,
light binning, stream compaction keys.

## 1. Bitonic (small or power-of-two arrays)
```hlsl
// one pass of the network; dispatch for k = 2..N (doubling), j = k/2..1 (halving)
[numthreads(256,1,1)] void BitonicStep(uint i : SV_DispatchThreadID) {
  uint l = i ^ j;
  if (l > i) {
    bool asc = (i & k) == 0;
    uint a = keys[i], b = keys[l];
    if ((a > b) == asc) { keys[i] = b; keys[l] = a; }
  }
}
```
O(n log^2 n) work; do the inner steps for j < groupsize in groupshared memory in one dispatch.
Fine up to roughly 64K elements; pad to a power of two with max keys.

## 2. LSD radix sort (large arrays)
Per 4-8 bit digit pass:
1. **Count**: each workgroup builds a histogram of digits for its block (groupshared atomics).
2. **Scan**: exclusive prefix sum over (digit, block) counts, giving global offsets.
3. **Scatter**: each element writes to `offset[digit][block] + local rank`; local rank via a
   per-workgroup scan or wave intrinsics (`WavePrefixCountBits`, `WaveMatch`).
32-bit keys with 8-bit digits = 4 passes; ping-pong key (and payload) buffers. Sort only as many
bits as needed (16-bit depth keys = 2 passes).

## 3. Use a library
FidelityFX Parallel Sort (D3D12/Vulkan HLSL), CUB `DeviceRadixSort` / OneSweep (CUDA),
`wgpu_sort` / WebGPU radix implementations. Writing your own is mainly for learning or tight
integration.

## Gotchas
- Radix sort is stable only if scatter preserves order within a digit (ranking must be stable).
- Float keys: flip bits (`k ^ (k >> 31 ? 0xFFFFFFFF : 0x80000000)`) so they sort as uints.
- UAV barriers between every pass; indirect dispatch if the count is GPU-generated.

## Verify
- [ ] Validate against a CPU sort on random, sorted, reversed and all-equal inputs.
- [ ] Time per million keys versus the library baseline.
