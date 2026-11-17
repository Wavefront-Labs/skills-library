---
id: computing-software.software-engineering.zig.optional-orelse
name: optional-orelse
category: computing-software
field: software-engineering
product: zig
tags: [zig, optional-orelse, zig-optionals, orelse, optional-unwrap, null-optional]
level: intro
status: docs-checked
description: "Unwrap Zig optionals with orelse, .?, if capture and while capture, and know the cost of optional pointers."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# orelse, .? and optional unwrapping
**Goal:** handle absence without exceptions.

```zig
var x: ?u32 = null;
const a = x orelse 0;                 // default
const b = x orelse return error.Missing;   // early exit
const c = x.?;                        // asserts non-null (panic in safe modes, UB in unsafe)
if (x) |v| use(v);
x = 5;
```
- `?T` is `T` plus a flag; `?*T`, `?[]T`... pointer optionals use the null address and are the same size as `*T` for single pointers and C-pointer-compatible.
- Optional chaining by hand: `if (a) |p| if (p.next) |n| ...`.
- `orelse unreachable` is equivalent to `.?`.
- Comparing: `x == null`, `x != null` is fine; `x == 5` works (coerces 5 to `?u32`).
- Optional of optional is allowed; `??T` is rarely wanted.

## Gotchas
- Using `.?` in library code on external input is a crash; return an error instead.
- Hash map `get` returns `?V`; `getPtr` returns `?*V` for in-place update.

## Self-check
Write `firstEven(xs) ?u32`, test both some and none cases, and use `orelse` at the call site.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: optionals, orelse, .?, pointer optionals (language reference optionals section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
