---
id: computing-software.software-engineering.zig.vector-simd
name: vector-simd
category: computing-software
field: software-engineering
product: zig
tags: [zig, vector-simd, zig-vectors, vector, splat, reduce, shuffle, simd]
level: advanced
status: docs-checked
description: "Write portable SIMD in Zig with @Vector, @splat, @reduce, @shuffle and @select, and convert between arrays and vectors."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/simd.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @Vector arithmetic, splat, reduce and shuffle
**Goal:** use SIMD without intrinsics.

```zig
const V = @Vector(4, f32);
const a: V = .{ 1, 2, 3, 4 };
const b: V = @splat(2.0);          // result type inferred
const c = a * b + a;               // element-wise
const sum = @reduce(.Add, c);      // horizontal sum
const mask = a > b;                // @Vector(4, bool)
const picked = @select(f32, mask, a, b);
const arr: [4]f32 = c;             // vector to array coercion
const rev = @shuffle(f32, a, undefined, @Vector(4, i32){ 3, 2, 1, 0 });
```
- `@Vector(len: comptime_int, Element: type)`. Math operators on a mixture of scalars and vectors are prohibited; use `@splat`. `@reduce` and array indexing syntax convert vectors to scalars.
- Vectors support assignment to and from fixed-length arrays with comptime-known length.
- `@shuffle(E, a, b, mask)`: `mask` is a comptime `@Vector(n, i32)`; non-negative entries pick from `a`, negative entries pick from `b` (use `~` so both start at 0).
- `std.simd.suggestVectorLength(T)` returns `?comptime_int` for the target.
- Select CPU features with `-Dcpu=...` through `standardTargetOptions`.

## Gotchas
- Vectors longer than the native SIMD size compile to multiple SIMD instructions; if an operation has no SIMD support on the target, the compiler operates on one element at a time. Very long vectors (e.g. 2^20) may crash current compilers.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Vectors section, `@shuffle` and `@Vector` of the language reference and `std.simd.suggestVectorLength` (return type `?comptime_int`). Fixed: `suggestVectorLength` is not `?usize`. Removed: element-type list, `-mcpu=native`, LLVM and float-associativity claims.

Method: documentation only; no commands were run.

## Self-check
Sum a 1024-element f32 array with 8-wide vectors plus scalar tail and compare to the scalar result within tolerance.
