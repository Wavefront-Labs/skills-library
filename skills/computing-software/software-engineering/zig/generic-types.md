---
id: computing-software.software-engineering.zig.generic-types
name: generic-types
category: computing-software
field: software-engineering
product: zig
tags: [zig, generic-types, zig-generics, comptime-type-param, returns-type, generic-struct]
level: practitioner
status: docs-checked
description: "Write generic containers in Zig as functions that take comptime type parameters and return struct types."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/array_list.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic data structures as functions returning types
**Goal:** build reusable containers without templates.

```zig
fn Stack(comptime T: type) type {
    return struct {
        const Self = @This();
        items: std.ArrayList(T) = .empty,
        pub fn push(self: *Self, a: std.mem.Allocator, v: T) !void {
            try self.items.append(a, v);
        }
        pub fn pop(self: *Self) ?T { return self.items.pop(); }
        pub fn deinit(self: *Self, a: std.mem.Allocator) void { self.items.deinit(a); }
    };
}
const IntStack = Stack(i32);
```
- A function returning `type` is `TitleCase` by the style guide. In 0.15.1 `std.ArrayList(T)` is the unmanaged form (`.empty`, allocator per call), so the container above stores no allocator.
- Add static checks with `@compileError` for unsupported `T`.
- Zig infers the debugging name (e.g. `"Stack(i32)"`) from the function name and arguments; assign the type to a `const` to give it an explicit name.

## Gotchas
- Put code that does not depend on `T` in plain helper functions so it is not duplicated per instantiation.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Generic Data Structures section of the language reference (anonymous struct returned from a function, inferred name); `ArrayList` unmanaged `.empty`, `append(a, v)`, `pop()` returning `?T` and `deinit(a)` in array_list.zig. Fixed: the example used `ArrayListUnmanaged` with `.{}`, now `ArrayList` with `.empty`. Removed: type-identity and compile-time claims.

Method: documentation only; no commands were run.

## Self-check
Instantiate `Stack(u8)` and `Stack(f32)` and confirm `@TypeOf` differs; push/pop under `std.testing.allocator`.
