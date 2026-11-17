---
id: computing-software.software-engineering.zig.std-math
name: std-math
category: computing-software
field: software-engineering
product: zig
tags: [zig, std-math, zig-std-math-meta, maxint, clamp, gcd, checked-math]
level: practitioner
status: docs-checked
description: "Use std.math for constants, floor/ceil/round, pow, sqrt, trig, checked add and mul, gcd and clamp in Zig."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/math.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/math/big/int.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.math: constants, rounding, safe arithmetic
**Goal:** numeric helpers.

```zig
const pi = std.math.pi;           const e = std.math.e;
std.math.maxInt(u32);             std.math.minInt(i8);
@floor(x); @ceil(x); @round(x); @trunc(x); @sqrt(x); @abs(x);   // builtins
std.math.pow(f64, 2, 10);         std.math.sin(x); std.math.log2(x);
std.math.clamp(v, 0, 100);        std.math.sign(x);
std.math.divCeil(u32, 7, 2) catch unreachable;
std.math.gcd(12, 18);             std.math.isPowerOfTwo(n);
std.math.ceilPowerOfTwo(u32, n) catch return error.TooBig;
std.math.order(a, b);             // .lt .eq .gt
std.math.lerp(a, b, t);
std.math.approxEqRel(f64, a, b, 1e-9);
```
- Builtins operate on floats and vectors: `@sin`, `@cos`, `@exp`, `@log`, `@mulAdd`, `@min`, `@max`.
- Checked arithmetic: `std.math.add/sub/mul/shl` return error on overflow; `std.math.cast(T, x)` returns `?T`.
- Big integers: `std.math.big.int.Managed` (arbitrary precision, allocator based).
- Complex numbers `std.math.Complex(f32)`.

## Gotchas
- `@intFromFloat` converts the integer part and is safety-checked illegal behavior when the value does not fit the destination type.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `pi`, `e`, `maxInt`, `minInt`, `pow`, `sin`, `log2`, `clamp`, `sign`, `divCeil`, `gcd`, `isPowerOfTwo`, `ceilPowerOfTwo`, `order`, `lerp`, `approxEqRel`, checked `add`/`sub`/`mul`/`shl`, `cast` returning `?T`, `big.int.Managed`, `Complex`; the float builtins and `@intFromFloat` text in the language reference. Removed: the integer-`sqrt` remark.

Method: documentation only; no commands were run.

## Self-check
Compute `std.math.cast(u8, 300)` (null) and `maxInt(u8)`; check `approxEqRel` for `0.1+0.2` vs `0.3`.
