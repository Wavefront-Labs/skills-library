---
id: computing-software.software-engineering.zig.slice-operations
name: slice-operations
category: computing-software
field: software-engineering
product: zig
tags: [zig, slice-operations, zig-arrays-slices, slice-bounds, slicing, const-slice]
level: practitioner
status: docs-checked
description: "Create and use Zig slices with a[start..end], runtime bounds checks, open ends, const slices and mutation through slices."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slices, slicing and bounds
**Goal:** pass sequences as `[]T` and slice safely.

```zig
var arr = [_]u8{ 10, 20, 30, 40 };
const s: []u8 = arr[1..3];        // {20, 30}, end exclusive
const t = arr[2..];               // to the end
const all: []const u8 = &arr;     // pointer-to-array coerces to slice
s[0] = 99;                        // writes through to arr
const len = s.len;
```
- A slice is `{ptr, len}`; `[]const T` for read-only (default for inputs).
- Out-of-range slice bounds are safety-checked illegal behavior (see the Illegal Behavior section).
- `std.mem.copyForwards` and `copyBackwards` (`comptime T, dest: []T, source: []const T`), `@memcpy(dest, source)` (non-overlapping), `@memmove(dest, source)` (regions may overlap), `@memset(dest, elem)`.
- `std.mem.eql(u8, a, b)` compares contents (`==` compares nothing useful for slices).

## Gotchas
- Slicing does not copy; the slice dangles if the array or list reallocates (`ArrayList.append` can invalidate old slices).
- `@memcpy` needs equal lengths when both sides provide one, and the regions must not overlap; use `@memmove` when they might.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `@memcpy`, `@memmove` and `@memset` text in the language reference, and `std.mem.copyForwards`, `copyBackwards` and `eql` signatures in mem.zig. Removed: the exact panic messages and the array-slice pointer-type remark.

Method: documentation only; no commands were run.

## Self-check
Slice an `ArrayList` items, append until it reallocates, and note why holding the old slice is a bug.
