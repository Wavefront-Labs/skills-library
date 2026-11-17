---
id: computing-software.computer-graphics-engineering.shader-programming.gpu-atomics-and-lock-free-patterns
name: gpu-atomics-and-lock-free-patterns
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, compute-shader-patterns, gpu-atomics, interlocked, lock-free, memory-model, wave-intrinsics, compute-shader]
level: advanced
status: docs-checked
description: "Use GPU atomics correctly: atomic add/min/max/CAS, packing depth+payload into 64-bit atomics, spin-lock hazards, memory scopes, and the wave-aggregation optimisation."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/khr/GL_KHR_memory_scope_semantics.txt", "https://github.com/microsoft/DirectX-Specs/blob/master/d3d/HLSL_SM_6_6_Int64_and_Float_Atomics.md", "https://docs.vulkan.org/spec/latest/appendices/memorymodel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics and lock-free patterns on GPU

## 1. Operations
GLSL: `atomicAdd, atomicMin, atomicMax, atomicAnd, atomicOr, atomicXor, atomicExchange,
atomicCompSwap` on `uint/int` in SSBOs, shared memory and `r32ui` images.
HLSL: `InterlockedAdd/Min/Max/And/Or/Xor/Exchange/CompareExchange` on RWBuffers/groupshared.
64-bit: `GL_EXT_shader_atomic_int64` / SM 6.6 64-bit integer atomics (for example `InterlockedMax` on `uint64_t`).
Float add: `VK_EXT_shader_atomic_float`; SM 6.6 adds only bitwise floating-point compare-exchange/compare-store, not float add.

## 2. Classic patterns
- **Counters / append**: `atomicAdd(count, 1)` returns the old value as a slot index.
- **Min-depth with payload** (for example a visibility-buffer software rasteriser): pack
  `(depth << 32) | triangleId` into 64 bits and `atomicMax` (reversed-Z) so the nearest wins and
  carries its payload in one op.
- **Float min/max** with uint atomics: for non-negative floats, `floatBitsToUint` preserves order;
  for signed, flip bits (`f >= 0 ? bits | 0x80000000 : ~bits`).
- **Linked lists** (OIT): `node = atomicAdd(nodeCounter, 1); prev = imageAtomicExchange(head, p, node)`.
- **Bounded queues**: separate head/tail counters; consumers check `idx < tail` after reading.

## 3. Aggregate first
One atomic per wave (`WaveActiveSum`, `WavePrefixSum`, then lane 0 does `InterlockedAdd`) is the
single biggest atomic optimisation. Same for shared-memory privatisation before global atomics.

## 4. Spin locks are dangerous
A lane waiting on a lock held by another lane in the same subgroup can deadlock, because the API does not guarantee that
the lock holder makes progress while its neighbours spin. If unavoidable, structure as:
```glsl
bool done = false;
while (!done) {
    if (atomicCompSwap(lock[k], 0u, 1u) == 0u) { /* critical */ memoryBarrierBuffer(); atomicExchange(lock[k], 0u); done = true; }
}
```
(lock and unlock inside the same iteration). Prefer redesigning to avoid locks (per-thread
ownership, sorting by key, or 64-bit packing).

## 5. Memory model
- Atomics are atomic, not ordering barriers. Use `memoryBarrierBuffer()` / `DeviceMemoryBarrier()`
  and Vulkan memory model semantics (`atomicStore(..., gl_ScopeDevice, gl_StorageSemanticsBuffer,
  gl_SemanticsRelease)`) when other invocations read data published by an atomic flag.
- `coherent`/`globallycoherent` on buffers you poll across workgroups.

## Gotchas
- Atomic throughput collapses when all lanes hit one address; check contention in profiles.
- Image atomics need a format with `STORAGE_IMAGE_ATOMIC_BIT`; check `vkGetPhysicalDeviceFormatProperties`.
- Results depending on atomic order are non-deterministic; never use them for reproducible output.

## Verify
- [ ] Stress test with millions of operations compares against CPU totals.
- No hangs on all target vendors; run with validation enabled.

## Checked

Checked 2026-10-26 against GLSL 4.60 specification, GL_KHR_memory_scope_semantics, DirectX-Specs HLSL Shader Model 6.6 and its int64/float atomics spec (main), Vulkan-Docs formats chapter. Confirmed: GLSL atomic functions and the `atomicStore(..., scope, storage, semantics)` form from GL_KHR_memory_scope_semantics; SM 6.6 adds 64-bit integer atomics and only bitwise floating-point CompareExchange/CompareStore; `STORAGE_IMAGE_ATOMIC_BIT` for image atomics. Corrected: SM 6.6 does not provide float add. Removed as unconfirmed: the lockstep-execution explanation of lock deadlocks (now stated as a progress-guarantee caveat), 'Nanite-style'.

Method: documentation only; no commands were run.
