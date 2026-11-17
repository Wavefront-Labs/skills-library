---
id: computing-software.game-programming.game-engine-architecture.memory-alignment-and-padding
name: memory-alignment-and-padding
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, memory-alignment, struct-padding, simd, game-programming]
level: practitioner
status: draft
description: "Control alignment and padding: alignof/alignas, struct member ordering, SIMD and GPU buffer alignment rules, aligned allocation and packing pitfalls."
sources: ["https://en.cppreference.com/w/cpp/language/object#Alignment", "https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-packing-rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alignment and padding

**Goal:** structs that are small, cache-friendly and correctly aligned for CPU SIMD and GPU buffers.

## Basics
- Each type has `alignof(T)`; the compiler pads members to their alignment and the struct size to
  a multiple of the largest member alignment.
```cpp
struct Bad  { bool a; double b; bool c; };   // 24 bytes
struct Good { double b; bool a; bool c; };   // 16 bytes: order members largest to smallest
static_assert(sizeof(Good) == 16);
```
- `alignas(16) float v[4];` for SSE, `alignas(32)` for AVX, `alignas(64)` to start on a cache line.
- Allocate over-aligned types with C++17 aligned `new` (automatic for `alignas` > default), or
  `_aligned_malloc`/`std::aligned_alloc` (size must be a multiple of alignment for the latter).

## GPU buffer rules
- HLSL constant buffers: 16-byte registers; a `float3` followed by a `float` packs together, but a
  member never straddles a 16-byte boundary. Arrays in cbuffers pad each element to 16 bytes.
- GLSL `std140`: `vec3` aligned to 16 bytes; arrays of scalars have 16-byte stride. `std430`
  (SSBOs) removes the array padding but `vec3` is still 16-aligned.
- Mirror shader structs in C++ with explicit padding fields and `static_assert(offsetof(...))`.

## Packing pitfalls
- `#pragma pack(1)` gives unaligned members: slower, and atomic/SIMD ops on them can fault.
  Use it only for serialisation views, then copy into aligned structs.
- Bitfields have implementation-defined layout; don't serialise them directly.
- Mixed 32/64-bit platforms differ in `long` and pointer size; use fixed-width types in data files.

## Verify
- `static_assert(sizeof/alignof/offsetof)` for every struct shared with GPU or files.
- Compile with `-Wpadded` (GCC/Clang) on hot structs to see padding.
