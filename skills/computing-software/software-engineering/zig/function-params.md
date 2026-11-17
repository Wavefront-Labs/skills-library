---
id: computing-software.software-engineering.zig.function-params
name: function-params
category: computing-software
field: software-engineering
product: zig
tags: [zig, function-params, zig-functions, parameter-immutability, pass-by-reference, const-pointer-param]
level: practitioner
status: docs-checked
description: "Understand that Zig parameters are immutable, how large values are passed by const reference under the hood, and when to pass pointers."
sources:
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parameters, immutability and pass-by-value
**Goal:** write function signatures that are fast and unambiguous.

- Parameters are immutable. To change a value take a pointer: `fn inc(p: *i32) void { p.* += 1; }`, or copy into a local `var`.
- Primitives such as integers and floats are copied (passed by value). For structs, unions and arrays Zig may choose to copy or pass by reference, whichever it decides is faster; this is possible in part because parameters are immutable (Pass-by-value Parameters section). Extern functions follow the C ABI for structs and unions by value.
- Prefer `const` pointers (`*const T`) or slices (`[]const T`) for read-only large inputs.
- Return type may be `!T`, `?T`, a comptime-computed type, or `anytype`-driven (`@TypeOf`).
- Function parameters can be `comptime` (value known at compile time) and `anytype` for generics.

```zig
fn sum(xs: []const i32) i32 {
    var t: i32 = 0;
    for (xs) |x| t += x;
    return t;
}
```
## Gotchas
- Parameters are immutable, so assigning to one is a compile error; copy into a local `var` first.
- Because the compiler may pass a large `b: T` by reference, `fn f(a: *T, b: T)` called with the same object as `a.*` and `b` may observe changes through `a`; take an explicit copy if you need a snapshot.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Functions section and Pass-by-value Parameters text of the language reference. Removed: the exact error message, the unused-parameter rule and the 'known hazard' wording.

Method: documentation only; no commands were run.

## Self-check
Write `swap(a: *i32, b: *i32)` and test it; try assigning to a parameter and read the error.
