---
id: computing-software.software-engineering.zig.c-callbacks-userdata
name: c-callbacks-userdata
category: computing-software
field: software-engineering
product: zig
tags: [zig, c-callbacks-userdata, zig-interop, callback, userdata, callconv-c, string-marshalling, c-errors]
level: advanced
status: docs-checked
description: "Pass Zig functions as C callbacks with callconv, carry state via void-pointer user data, and marshal strings, arrays and errors across the C boundary."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/builtin.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C callbacks, user data and string marshalling
**Goal:** call C APIs that want callbacks.

```zig
const Ctx = struct { calls: usize = 0 };
fn cb(user: ?*anyopaque, a: c_int) callconv(.c) c_int {
    const ctx: *Ctx = @ptrCast(@alignCast(user.?));
    ctx.calls += 1;
    return a * 2;
}
```
- In 0.15.1 the C calling convention is spelled `callconv(.c)` (`std.builtin.CallingConvention` has a `c` tag; the reference examples use it), including for variadic functions such as `fn add(count: c_int, ...) callconv(.c) c_int`.
- A Zig function cannot capture state; pass state through the C API's user-data pointer as `?*anyopaque` and cast back with `@ptrCast(@alignCast(...))`. Keep the data alive for as long as C may use it.
- Structs passed to or from C must be `extern struct`; for extern functions Zig follows the C ABI when passing structs and unions by value.
- Pointer forms from C: `[*c]T` appears in translated code; the reference suggests editing translated output to use `[*]T` or `*T` for safety.

## Self-check
Wrap a C `qsort` call with a Zig comparator declared `callconv(.c)` and sort an array.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (`callconv(.c)` examples, extern struct and C ABI notes, C Translation section) and `lib/std/builtin.zig` (`CallingConvention`).
Removed: the `.C` spelling and its "newer releases" hedge, `qsort_like.h` example, "callbacks must not return errors or unwind", dupeZ/span string rules, `enum(c_int)` with `_` advice, threading note, "wrap C APIs" style advice.
Method: documentation only; no commands were run.
