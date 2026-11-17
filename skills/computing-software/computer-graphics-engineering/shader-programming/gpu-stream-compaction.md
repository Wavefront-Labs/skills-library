---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-stream-compaction
name: gpu-stream-compaction
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, stream-compaction, prefix-sum, wave-intrinsics, append-buffer, compute-shader, gpgpu]
level: advanced
status: draft
description: "Compact sparse GPU data in compute shaders: predicate + prefix-sum scatter, wave-intrinsic ballot compaction, atomic append buffers, and writing indirect counts."
sources: ["https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_ShaderModel6.md", "https://docs.vulkan.org/guide/latest/subgroups.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stream compaction

Input: N elements, a predicate per element. Output: the passing elements packed contiguously, plus
the count. Used for culling lists, particle alive lists, ray queues, light lists.

## 1. Atomic append (simplest)
```hlsl
RWStructuredBuffer<uint> outList; RWByteAddressBuffer counter;
[numthreads(64,1,1)] void CS(uint id : SV_DispatchThreadID) {
    if (id < N && Keep(id)) { uint slot; counter.InterlockedAdd(0, 1, slot); outList[slot] = id; }
}
```
Order is not preserved; one global atomic per survivor contends when many pass.

## 2. Wave-aggregated atomics (fast, order within wave)
```hlsl
bool keep = id < N && Keep(id);
uint waveCount = WaveActiveCountBits(keep);
uint waveOffset = WavePrefixCountBits(keep);
uint base = 0;
if (WaveIsFirstLane()) counter.InterlockedAdd(0, waveCount, base);
base = WaveReadLaneFirst(base);
if (keep) outList[base + waveOffset] = id;
```
GLSL: `subgroupBallot`, `subgroupBallotBitCount`, `subgroupBallotExclusiveBitCount`,
`subgroupElect`, `subgroupBroadcastFirst` (requires `GL_KHR_shader_subgroup_ballot`).
One atomic per wave instead of per element: 32-64x fewer atomics.

## 3. Prefix-sum scatter (deterministic, order preserved)
1. Pass 1: write flags `f[i] = keep ? 1 : 0`.
2. Exclusive scan of flags -> `idx[i]` (block scan in shared memory + block sums scan + add back,
   or a single-pass decoupled look-back scan).
3. Pass 3: `if (f[i]) out[idx[i]] = in[i]`; count = `idx[N-1] + f[N-1]`.
Use when output order must be stable (deterministic replay, sorted inputs).

## 4. Feeding indirect draws/dispatches
Write the count straight into the indirect args buffer:
- Draw: `args.instanceCount` or `vertexCount`; Dispatch: `groupCountX = (count + 63) / 64`
  computed in a tiny 1-thread dispatch after the compaction.
- `vkCmdDrawIndirectCount` / `ExecuteIndirect` with a count buffer avoid the extra pass.
Barrier from compute write to `INDIRECT_COMMAND_READ` before the draw.

## Gotchas
- Reset the counter each frame (copy zero or a clear dispatch) with a barrier before use.
- Wave size varies (32/64, or 4-128 on mobile); never hardcode; query `WaveGetLaneCount()`.
- Inactive lanes (out-of-range threads) must still participate correctly in wave ops; compute the
  predicate for all lanes and mask.

## Verify
- [ ] Compare output count and contents against a CPU filter for random inputs.
- [ ] Profile atomics: wave-aggregated version shows far fewer atomic ops.
