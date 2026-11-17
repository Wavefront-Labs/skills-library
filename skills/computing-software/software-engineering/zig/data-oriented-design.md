---
id: computing-software.software-engineering.zig.data-oriented-design
name: data-oriented-design
category: computing-software
field: software-engineering
product: zig
tags: [zig, data-oriented-design, zig-performance, struct-of-arrays, cache-locality, index-handles, soa]
level: sme
status: docs-checked
description: "Apply data-oriented design in Zig with MultiArrayList struct-of-arrays, index handles, arena reset and explicit type sizes."
sources:
  - https://ziglang.org/documentation/master/
  - https://raw.githubusercontent.com/ziglang/zig/master/lib/std/multi_array_list.zig
  - https://raw.githubusercontent.com/ziglang/zig/master/lib/std/heap/arena_allocator.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-oriented design and cache-friendly layouts
**Goal:** speed through memory layout.

- Prefer arrays of homogeneous data over pointer graphs: `std.MultiArrayList(Entity)` stores each field in its own array. `items(.field)` returns the slice for one field. When reading several fields call `slice()` first: its cached start pointers are not stored in the list itself to keep the list small.
- Replace pointers with 32-bit indexes into arrays (for example a non-exhaustive `enum(u32) { _ }` as a typed handle) so data stays movable.
- Arenas per phase: `ArenaAllocator.reset(.retain_capacity)` keeps the memory for reuse (it returns a `bool`).
- Struct layout: the language reference says Zig gives no guarantee about the order or size of a plain `struct`'s fields, though fields are ABI-aligned. An `extern struct` has C ABI layout. Inspect with `@sizeOf`, `@alignOf` and `@offsetOf`.
- Use small integer tag types for hot data (`enum(u8)`).
- Specialise hot loops with `comptime` parameters and `inline for` over small fixed sets; `@Vector` exists for SIMD over contiguous columns.

## Gotchas
- Index handles lose compile-time lifetime checking; consider generation counters in Debug builds.
- Removing from a MultiArrayList invalidates pointers to fields of the removed element, and growth can reallocate, so avoid holding pointers into it.

## Self-check
Benchmark updating positions for 1M entities as `[]Entity` versus `MultiArrayList` in ReleaseFast.

## Checked

2026-11-08. Read: multi_array_list.zig and arena_allocator.zig by targeted search (items, slice, reset/retain_capacity, invalidation notes); language reference sections on struct layout, extern struct, @sizeOf/@alignOf/@offsetOf, inline for, @Vector and non-exhaustive enums by search (partial read of a very large page).
Removed: the claim that the Zig compiler uses index handles, halved-memory claim, perf stat advice, "default structs are reordered" (the reference only says no guarantee), std docs source (JavaScript-rendered, not read).
Method: documentation only; no commands were run.
