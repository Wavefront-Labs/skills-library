---
id: computing-software.software-engineering.zig.type-reflection
name: type-reflection
category: computing-software
field: software-engineering
product: zig
tags: [zig, type-reflection, zig-comptime, typeinfo, hasdecl, std-meta, reflection]
level: advanced
status: gated
description: "Inspect Zig types at comptime using @typeInfo, @hasDecl, @field and std.meta to write generic serializers and checkers."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://ziglang.org/documentation/0.15.2/std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type reflection with @typeInfo and std.meta
**Goal:** write code generic over struct shapes.

```zig
fn dump(value: anytype) void {
    const T = @TypeOf(value);
    switch (@typeInfo(T)) {
        .@"struct" => |info| inline for (info.fields) |f| {
            std.debug.print("{s} = {any}\n", .{ f.name, @field(value, f.name) });
        },
        .int, .comptime_int => std.debug.print("int {d}\n", .{value}),
        else => @compileError("unsupported " ++ @typeName(T)),
    }
}
```
- Tag spellings of `std.builtin.Type` changed: older releases `.Struct`, `.Int`, `.Pointer`; newer ones lowercase with `@"struct"` (the 0.15.2 language reference uses lowercase tags such as `.@"struct"`). Match your compiler version.
- Useful: `@hasDecl(T, "name")`, `@hasField`, `@field(v, "name")` read/write by comptime string, `@typeName`, `@TypeOf`, `std.meta.fields(T)`, `std.meta.FieldEnum(T)`, `std.meta.Child`, `std.meta.Tag`. (gated: unconfirmed, source is paywalled or blocked)
- Constructing types: `@Type(.{...})` in the 0.15.2 language reference; the master docs replace it with builtins such as `@Int` and `@Tuple`, so check the docs for your compiler version.
- `inline for` is required to iterate fields because each field has a different type.

## Gotchas
- Reflection is comptime only; runtime field-by-name access needs a `switch` on `std.meta.stringToEnum` of `FieldEnum`.
- Decl lookup does not trigger analysis of the function, so `@hasDecl` cannot detect compile errors inside.

## Self-check
Write `fieldNames(T)` returning `[]const []const u8` at comptime and test on a 3-field struct.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: @typeInfo lowercase tags, @Type in 0.15.2, @Int/@Tuple in master, @hasDecl, @hasField, @typeName (language reference).
- Removed or changed: the unconfirmed hedges on tag spelling and @Type.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
