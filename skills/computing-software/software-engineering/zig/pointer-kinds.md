---
id: computing-software.software-engineering.zig.pointer-kinds
name: pointer-kinds
category: computing-software
field: software-engineering
product: zig
tags: [zig, pointer-kinds, zig-pointers, single-item-pointer, many-item-pointer, c-pointer]
level: practitioner
status: docs-checked
description: "Distinguish *T, [*]T, [*c]T and slices in Zig, with dereference syntax, pointer arithmetic and when each is used."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single-item, many-item and C pointers
**Goal:** know which pointer type to use and how to convert.

| Type | Meaning |
|---|---|
| `*T` | pointer to exactly one T; deref `p.*` |
| `[*]T` | unknown number of items; index and arithmetic, no `.len` |
| `[]T` | slice: ptr + len (preferred) |
| `[*c]T` | C pointer; nullable and may be unaligned, for translate-c only |
| `?*T` | optional pointer (null is zero address, same size as `*T`) |

```zig
var x: u32 = 5;
const p: *u32 = &x;
p.* += 1;
const arr = [_]u8{ 1, 2, 3 };
const many: [*]const u8 = &arr;      // coerce array pointer to many-pointer
const slice = many[0..3];            // back to a slice
```
- `*T` cannot be null; use `?*T`. Pointer arithmetic exists only on `[*]T` (`many + 1`) via indexing or slicing.
- `*[N]T` (pointer to array) coerces to `[]T` and `[*]T`.
- `@ptrCast`, `@alignCast`, `@intFromPtr`, `@ptrFromInt` convert between kinds (use sparingly).

## Gotchas
- Dangling pointers to stack locals returned from a function are not detected by the compiler; Debug mode may overwrite with 0xaa.
- `p.*` after `defer allocator.destroy(p)` is use-after-free.

## Self-check
Take a pointer into an array element, mutate through it, and verify the array changed; assign null to `*u32` and read the error.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: *T, [*]T, [*c]T, ?*T, slices, 0xaa undefined fill (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
