---
id: computing-software.software-engineering.zig.integer-widths
name: integer-widths
category: computing-software
field: software-engineering
product: zig
tags: [zig, integer-widths, zig-primitives, u8, i32, usize, intcast, truncate]
level: practitioner
status: docs-checked
description: "Choose among Zig iN/uN arbitrary-width integers, usize/isize and c_int, and convert between them safely with casts."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arbitrary-width integers and usize
**Goal:** pick integer types deliberately and convert without silent loss.

- Any width from `u1` to `u65535` exists (maximum 65535 bits per the 0.15.2 language reference): `u3`, `i7`, `u128`.
- `usize`/`isize` match pointer width; indexes and lengths are `usize`.
- C ABI types: `c_int`, `c_uint`, `c_long`, `c_char`, `c_short`, `c_longlong`.

## Conversions (result type is inferred from context)
```zig
const big: u32 = 300;
const a: u8 = @intCast(big);      // safety-checked: panics in Debug/ReleaseSafe if it does not fit
const b: u8 = @truncate(big);     // keeps low bits, never checked
const c: u64 = big;               // widening is implicit
const d = @as(i64, big);          // explicit coercion
const idx: usize = @intCast(some_i32);
```
- `@intCast` needs a known result type; when none exists write `@as(u8, @intCast(x))`.
- Mixed signedness is never implicit: `i32` to `u32` requires `@intCast` (checked) or `@bitCast` (reinterpret).
- `@intFromBool`, `@intFromEnum`, `@intFromFloat`, `@floatFromInt`, `@intFromPtr` are the other int-conversion builtins.

## Gotchas
- Before the 0.11 builtin overhaul `@intCast(T, x)` took the type first; old tutorials show that form and it no longer compiles.
- Shifting needs the shift amount type `Log2Int(T)` e.g. `u3` for `u8`: `x << @intCast(n)`.

## Self-check
Cast `@as(u32, 300)` to u8 with `@intCast` in a Debug build and confirm the panic "integer cast truncated bits"; swap to `@truncate` and print 44.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: arbitrary-width integers, 65535 maximum, @intCast/@truncate builtins (language reference).
- Removed or changed: the verify-for-your-version hedge.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
