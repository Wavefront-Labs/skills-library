---
id: computing-software.software-engineering.zig.anytype-duck-typing
name: anytype-duck-typing
category: computing-software
field: software-engineering
product: zig
tags: [zig, anytype-duck-typing, zig-generics, anytype, duck-typing, comptime-constraint]
level: practitioner
status: docs-checked
description: "Accept any type with anytype in Zig, constrain it with @TypeOf checks and compile errors, and know the downsides."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Io.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# anytype and duck typing
**Goal:** write flexible functions and give good errors.

```zig
fn printAll(writer: anytype, items: anytype) !void {
    for (items) |it| try writer.print("{any}\n", .{it});
}
fn add(a: anytype, b: @TypeOf(a)) @TypeOf(a) { return a + b; }
```
- With `anytype` the parameter type is inferred at each call (use `@TypeOf` and `@typeInfo` to inspect it); errors surface inside the body at instantiation.
- Constrain with `@compileError`:
```zig
comptime {
    if (!@hasDecl(T, "write")) @compileError(@typeName(T) ++ " needs write()");
}
```
- `@TypeOf(a)` links parameter types; `@TypeOf(a, b)` performs peer type resolution.
- Result type from comptime-known data: `fn Foo(comptime T: type) ...` is explicit and more documentable than `anytype`.
- In 0.15.1 `std.Io.Writer` is a concrete type (Io/Writer.zig exists), so new std APIs take `*std.Io.Writer` rather than `anytype`.

## Gotchas
- An `anytype` parameter does not state its requirements; document them in `///`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Function Parameter Type Inference section of the language reference and the presence of `std.Io.Writer` in the 0.15.1 source. Removed: the tooling and function-pointer claims.

Method: documentation only; no commands were run.

## Self-check
Pass a type missing the required method and verify your custom compile error message shows up.
