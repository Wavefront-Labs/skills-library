---
id: computing-software.software-engineering.zig.struct-literals
name: struct-literals
category: computing-software
field: software-engineering
product: zig
tags: [zig, struct-literals, zig-structs, anonymous-struct, result-location, struct-init, designated-initializers]
level: practitioner
status: docs-checked
description: "Use Zig anonymous struct literals, result location inference, field defaults and update-by-copy idioms to build values concisely."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anonymous struct literals and result locations
**Goal:** write initialisers idiomatically.

```zig
const p: Point = .{ .x = 1, .y = 2 };
const q = Point{ .x = 1, .y = 2 };
fn draw(p: Point) void {}
draw(.{ .x = 3 });                       // type comes from the parameter; y uses default
var opts: Options = .{};                 // all defaults
const r = Rect{ .origin = .{ .x = 0, .y = 0 }, .size = .{ .w = 10, .h = 5 } };
var copy = p; copy.x = 9;                // struct update: copy then modify
const arr = [_]Point{ .{ .x = 1 }, .{ .x = 2 } };
return .{ .ok = true };                  // return type provides the struct type
```
- Result location semantics: the literal is constructed directly in its destination, so large structs are not copied through temporaries (also why `x = .{ .a = x.b, .b = x.a }` has aliasing hazards; build in a temp for swaps).
- `.{}` alone is an empty anonymous struct, convertible to any struct with all defaults, or an empty tuple/array.
- `.{ 1, 2, 3 }` is a tuple; it coerces to arrays `[3]T`.
- Missing non-default fields produce "missing struct field: name".
- Options-struct convention: functions take `Options` struct with defaults instead of many params (std uses this widely: `openFile(path, .{})`).

## Gotchas
- Anonymous struct literal assigned to `const` without a type is an anonymous struct type that does not coerce to named types in all contexts; annotate the type.
- Fields order in literal does not matter, but evaluation order is left to right.

## Self-check
Write a function with an options struct and call it with `.{}`, one field and all fields.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: anonymous struct literals, result locations, tuples (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
