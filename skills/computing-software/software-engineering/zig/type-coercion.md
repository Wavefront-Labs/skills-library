---
id: computing-software.software-engineering.zig.type-coercion
name: type-coercion
category: computing-software
field: software-engineering
product: zig
tags: [zig, type-coercion, zig-casting, peer-type-resolution, implicit-cast, coercion-rules]
level: practitioner
status: docs-checked
description: "Know which Zig conversions are implicit (widening, const-adding, array to slice) and how peer type resolution picks the result type."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit coercion and peer type resolution
**Goal:** predict when the compiler converts for you.

Implicit (safe, lossless) coercions:
- Narrow int to wider int of compatible signedness (`u8` to `u32`, `i8` to `i32`; `u8` to `i16` too).
- `T` to `?T`, `T` to `E!T`, `*T` to `*const T`, `*[N]T` to `[]T`/`[*]T`, `[N]T` const array to slice.
- `comptime_int`/`comptime_float` to any type that holds the value.
- Enum literal to enum; `*T` to `*anyopaque`; `noreturn` to anything.
- Tagged union to its enum tag type when the union is known.

Peer type resolution: in `if`/`switch`/`@max`/`a == b`/array literals/ternary-like expressions, the result type is the type all branches coerce to:
```zig
const x: u8 = 1; const y: u16 = 2;
const z = if (cond) x else y;        // u16
const m = @max(x, y);               // u16
```
- Not implicit: signed/unsigned mix, int to float, float to int, wider to narrower, `[]T` to `[*]T` (use `.ptr`), `[]const T` to `[]T`.
- Result location semantics: `const p: Point = .{ .x = 1 }` passes the type inward to the literal; `.{}` has no meaning without a known type.

## Gotchas
- `var i = 0;` gives comptime_int and fails at runtime use; annotate `var i: usize = 0`.
- Mixing `i32` and `u32` in arithmetic: "incompatible types" error; cast one with `@intCast`.

## Self-check
Add a `u8` and `u16` (works, widened), then an `i32` and `u32` (error), and fix with `@intCast`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: implicit coercions and peer type resolution (language reference type coercion section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
