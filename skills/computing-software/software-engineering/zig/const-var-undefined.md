---
id: computing-software.software-engineering.zig.const-var-undefined
name: const-var-undefined
category: computing-software
field: software-engineering
product: zig
tags: [zig, const-var-undefined, zig-variables, undefined, const, var, mutability]
level: intro
status: docs-checked
description: "Declare Zig constants and variables, initialise with undefined safely, and understand that unmutated var is a compile error."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# const, var and undefined
**Goal:** use `const` by default and `var` only when mutated.

```zig
const x: i32 = 5;       // immutable
var y: i32 = 0;         // mutable; must be mutated somewhere or compiler errors
y += 1;
var buf: [64]u8 = undefined;   // uninitialised memory, do not read before writing
```
- "local variable is never mutated" is a compile error (fix: change `var` to `const`).
- `undefined` means "unspecified bits". In Debug and ReleaseSafe builds the compiler fills it with `0xaa` bytes (an implementation feature, not guaranteed) to help find reads of uninitialised data; reading it is illegal behavior to rely on.
- `std.mem.zeroes(T)` gives a zero-initialised value; `.{}` gives a struct with all default field values; `std.mem.zeroInit` mixes both.
- Struct/array result literals infer from the declared type: `var p: Point = .{ .x = 1, .y = 2 };`.

## Gotchas
- `var a = [_]u8{1,2,3};` is `[3]u8`; the length is inferred by `[_]`.
- Assigning `undefined` to a `const` is pointless but legal at comptime.
- A `var` captured by a closure-like pattern does not exist: Zig has no closures; pass context explicitly.

## Self-check
Write `var n: u32 = 1;` without ever changing it and confirm the error; change to `const` and build.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: const/var, undefined and the 0xaa fill, never-mutated error (language reference).
- Removed or changed: narrowed the 0xaa claim to match the doc.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
