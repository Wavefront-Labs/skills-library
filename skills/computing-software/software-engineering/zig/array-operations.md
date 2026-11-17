---
id: computing-software.software-engineering.zig.array-operations
name: array-operations
category: computing-software
field: software-engineering
product: zig
tags: [zig, array-operations, zig-arrays-slices, array-concat, array-repeat, multidimensional-array]
level: intro
status: docs-checked
description: "Declare, initialise, concatenate and repeat Zig arrays at comptime and iterate multidimensional arrays."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref/test_arrays.zig
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref/test_multidimensional_arrays.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays, ++ and ** and multidimensional arrays
**Goal:** use fixed-size arrays correctly.

```zig
const a = [5]u8{ 1, 2, 3, 4, 5 };
const b = [_]u8{ 1, 2, 3 };            // length inferred
const z = [_]u8{0} ** 16;               // repeat: 16 zeros
const c = a ++ b;                       // concat, comptime-known operands (as in the language reference)
const grid = [3][4]i32{ [_]i32{0} ** 4, [_]i32{0} ** 4, [_]i32{0} ** 4 };   // arrays nest
var m: [2][2]u8 = undefined;
m[1][0] = 7;
const n = a.len;                        // comptime-known
```
- The language reference states that array concatenation `++` works if the values are known at compile time; `**` repeats a pattern (`"ab" ** 3`, `[_]u16{0} ** 10`), and string literals work with both.
- Multidimensional arrays are created by nesting arrays; `mat[1][0]` indexes the outer array, then the inner.
- Array of struct literal: `[_]Point{ .{ .x = 1, .y = 2 } }`.
- Arrays can be destructured.

## Gotchas
- `[_]u8{...}` needs every element to coerce to `u8`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Arrays, Multidimensional Arrays and Destructuring Arrays sections and test_arrays.zig / test_multidimensional_arrays.zig. Removed: value-semantics, bounds-check mode, zero-length and `void` array, stack-size claims.

Method: documentation only; no commands were run.

## Self-check
Build `[_]u8{0xAA} ** 4 ++ [_]u8{1}` and `std.testing.expectEqualSlices` against the expected 5 bytes.
