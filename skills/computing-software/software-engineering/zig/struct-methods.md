---
id: computing-software.software-engineering.zig.struct-methods
name: struct-methods
category: computing-software
field: software-engineering
product: zig
tags: [zig, struct-methods, zig-structs, struct-default-fields, self-parameter, init-deinit]
level: intro
status: docs-checked
description: "Declare Zig structs with default field values, methods via self parameter, namespaced declarations, and init/deinit conventions."
sources:
  - https://ziglang.org/documentation/0.15.1/#struct
  - https://ziglang.org/documentation/0.15.1/#Default-Field-Values
  - https://ziglang.org/documentation/0.15.1/#This
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Struct declarations, methods and default fields
**Goal:** structure data and behaviour the Zig way.

```zig
const Point = struct {
    x: f32 = 0,
    y: f32 = 0,
    pub const origin: Point = .{};
    pub fn init(x: f32, y: f32) Point { return .{ .x = x, .y = y }; }
    pub fn len(self: Point) f32 { return @sqrt(self.x * self.x + self.y * self.y); }
    pub fn scale(self: *Point, k: f32) void { self.x *= k; self.y *= k; }
};
var p = Point.init(3, 4);
p.scale(2);
const l = p.len();       // dot syntax for Point.len(p)
```
- Functions in a struct's namespace can be called with dot syntax; apart from that, struct methods are not special and can be referenced like any other declaration. Structs can have declarations and can have zero fields.
- Zig gives no guarantees about the order of fields or the size of a struct, but fields are guaranteed to be ABI-aligned. Use `extern struct` for a layout that matches the C ABI and `packed struct` for a well-defined layout equal to its backing integer.
- Each field may have a default value expression, evaluated at comptime, which lets the field be omitted in a struct literal. The reference warns to use defaults only when omitting the field cannot violate the struct's data invariants.
- `@This()` returns the innermost struct, union or enum type it appears in (at file scope, the file's own struct type).

## Self-check
Write a `Stack` with `init`, `push` and `deinit`, and test it with `std.testing.allocator`.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (struct, Default Field Values, extern struct, packed struct, @This) and `doc/langref/test_structs.zig`.
Removed: `init`/`deinit` convention, "no constructors, destructors or inheritance", the copy-versus-pointer gotcha, "all fields without defaults must be given".
Method: documentation only; no commands were run.
