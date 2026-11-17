---
id: computing-software.computer-graphics-engineering.shader-programming.compute-shaders-and-gpgpu-patterns
name: compute-shaders-and-gpgpu-patterns
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [shader-programming, compute-shader, gpgpu, thread-groups, shared-memory, parallel-reduction, prefix-sum, scan, particle-simulation, indirect-dispatch, groupshared, workgroup, memory-barrier]
level: advanced
status: docs-checked
description: "Write correct, efficient compute shaders: thread-group sizing, shared-memory reductions/prefix-sums, race conditions from missing barriers, and common GPGPU patterns (particle sim, culling)."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/sm5-attributes-numthreads", "https://registry.khronos.org/vulkan/specs/latest/html/vkspec.html#limits", "https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute shaders and GPGPU patterns

**Goal:** write compute shaders that are both correct (no races) and actually
use the hardware well — the two failure modes are silent wrong results
(missing a barrier) and silent slowness (bad thread-group sizing or memory access).

## Thread group sizing
- Dispatch is organised as `numGroups × threadsPerGroup`. Thread group size
  should be a multiple of the GPU's subgroup (warp/wavefront) size, which varies by vendor and GPU — query it
  (Vulkan reports `subgroupSize`) — a group size of 33 wastes lanes in a second subgroup.
  Limits: Vulkan guarantees `maxComputeWorkGroupInvocations` of at least 128 (256 in newer profiles);
  D3D `cs_5_0` allows up to 1024 threads per group (X*Y*Z, Z at most 64). Common default: 64 or 256 total
  threads per group (`8x8`, `16x16` for 2D image work).
- `numthreads(x,y,z)` (HLSL) / `local_size_x/y/z` (GLSL) declares this in the
  shader; the CPU-side `Dispatch(groupsX, groupsY, groupsZ)` call must account
  for the group size when covering a non-multiple-sized domain (dispatch extra
  groups, clamp/early-return threads outside the real range inside the shader).

## Shared memory and synchronisation
- `groupshared` (HLSL) / `shared` (GLSL) memory is visible to all threads in a
  **group** (not across groups) and is far faster than global memory for
  intra-group communication (reductions, local sorting, tile-based filtering).
- **Barriers are mandatory, not optional**, around any shared-memory
  read-after-write within a group: `GroupMemoryBarrierWithGroupSync()` (HLSL) /
  `barrier()` + `memoryBarrierShared()` (GLSL). Skipping it is a race condition
  that often "works" on one GPU/driver (execution happens to be lock-step enough)
  and silently corrupts results on another — a classic non-portable bug.
- Global (`RWStructuredBuffer`/`image` writes read elsewhere) hazards need
  `DeviceMemoryBarrierWithGroupSync` / GLSL `memoryBarrierBuffer()`, `memoryBarrierImage()` (or `groupMemoryBarrier()` for all
  of them), distinct from the group-shared barrier — using the wrong barrier scope is a
  common near-miss (compiles, passes on some data, fails on timing-sensitive cases).

## Parallel reduction
Summing/min/max across many elements using shared memory, halving active threads
each step:
```hlsl
groupshared float data[256];
data[tid] = input[globalID];
GroupMemoryBarrierWithGroupSync();
for (uint s = 128; s > 0; s >>= 1) {
    if (tid < s) data[tid] += data[tid + s];
    GroupMemoryBarrierWithGroupSync();   // every iteration, not just once
}
if (tid == 0) output[groupID] = data[0];
```
- The barrier **inside the loop** is required every iteration — threads at
  different loop stages would otherwise read partially-updated shared memory.
- For reductions across more elements than one group can hold: reduce per group,
  write partial results, then a second dispatch reduces those partials (classic
  two-pass reduction) rather than trying to synchronise across groups within one
  dispatch (there's no cross-group sync primitive within a single dispatch).

## Prefix sum / scan
Building an offset table (used for stream compaction — e.g. compacting a sparse
visibility list, or the clustered-lighting light-list building) needs a
**prefix sum**, not a simple reduction — classic work-efficient scan algorithms
(Blelloch) do it in shared memory per group then combine across groups with a
second pass, same two-pass structure as reduction above.

## Common GPGPU patterns
- **Particle simulation**: `RWStructuredBuffer` of particle state, one thread per
  particle, update in place — double-buffer (read from buffer A, write to buffer
  B, swap) if a particle's update depends on *other* particles' previous-frame
  state, to avoid read-after-write races within the same dispatch.
- **Indirect dispatch** (`DispatchIndirect`): dispatch dimensions come from a GPU
  buffer written by a previous pass (e.g. a compacted particle count) — avoids a
  CPU readback to know how many groups to launch.

## Verify
- [ ] Every shared-memory read-after-write within a group has the correct-scope
      barrier, verified on more than one GPU vendor if portability matters (races
      are often vendor/driver-dependent in whether they manifest).
- [ ] Thread group size is a multiple of the target hardware's warp/wavefront
      size; out-of-range threads at domain edges are clamped, not left to read/write OOB.
- [ ] Multi-group reductions/scans use a verified two-pass structure, not an
      attempted single-dispatch cross-group sync.
- [ ] Double-buffering confirmed present for any simulation where updates depend
      on other elements' previous state.

## Checked

Checked 2026-10-26 against GLSL 4.60 specification (barrier and memory barrier functions), Vulkan-Docs limits chapter (main, 2026-10-23), Microsoft numthreads page. Confirmed: `barrier()` semantics for compute workgroups, `memoryBarrierShared()`, `groupMemoryBarrier()` and their compute-only availability; `numthreads`/`local_size` limits for cs_5_0 (1024 threads, Z at most 64); `maxComputeWorkGroupInvocations` minimums (128, 256 in newer profiles). Algorithm descriptions (reduction, scan, double-buffering) are standard technique and were not checked against a source. Removed as unconfirmed: the per-vendor warp/wavefront sizes.

Method: documentation only; no commands were run.
