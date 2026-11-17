---
id: computing-software.software-engineering.zig.sentinel-alignment
name: sentinel-alignment
category: computing-software
field: software-engineering
product: zig
tags: [zig, sentinel-alignment, zig-pointers, sentinel-terminated, null-terminated, aligncast, std-mem-span]
level: advanced
status: gated
description: "Use Zig sentinel-terminated slices ([:0]u8, [*:0]u8), std.mem.span/sliceTo, and align(N)/@alignCast for C interop and SIMD."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel-terminated pointers and alignment
**Goal:** pass strings to C and handle alignment.

- `[:0]const u8` is a slice with a guaranteed 0 after `len` elements; `[*:0]const u8` is the C string pointer. String literals are `*const [N:0]u8` and coerce to both.
- Slice to sentinel: only via a checked operation: `const z = try alloc.dupeZ(u8, s);` or slicing with sentinel `buf[0..n :0]` (asserts `buf[n]==0`).
- C string to slice: `std.mem.span(ptr)` (returns `[:0]const u8`), or `std.mem.sliceTo(ptr, 0)`. (gated: unconfirmed, source is paywalled or blocked)
- Length of C string: `std.mem.len(ptr)`.

```zig
extern fn strlen(s: [*:0]const u8) usize;
const n = strlen("hello");           // literal coerces
```
## Alignment
- `align(N)` on types, variables and fields: `var buf: [1024]u8 align(64) = undefined;`
- `@alignOf(T)`, `@alignCast(ptr)` after `@ptrCast` from a less-aligned pointer; checked in safe modes.
- `std.mem.Alignment` is a newer enum type for allocator alignment arguments (0.14+, unconfirmed); `alloc.alignedAlloc(T, N, len)` older style.

## Gotchas
- Passing a `[]const u8` to a C function expecting `char*` without a sentinel is a classic buffer over-read; use `dupeZ`.
- `@ptrCast` loses alignment info; casting `*u8` to `*u32` needs `@alignCast`.

## Self-check
`dupeZ` a slice, pass it to `strlen`, compare to `s.len`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: sentinel-terminated pointers/slices, string literal type, align(N), @alignCast, @ptrCast (language reference).
- Removed or changed: nothing.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
