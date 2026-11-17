---
id: computing-software.software-engineering.zig.opaque-anyopaque
name: opaque-anyopaque
category: computing-software
field: software-engineering
product: zig
tags: [zig, opaque-anyopaque, zig-enums-unions, opaque, anyopaque, type-erasure, vtable]
level: advanced
status: docs-checked
description: "Model foreign handles in Zig with opaque {} and type-erase context pointers using *anyopaque with ptrCast and alignCast."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem/Allocator.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opaque types and anyopaque
**Goal:** hold C handles and implement runtime polymorphism.

```zig
const Handle = opaque {};                       // unknown (non-zero) size and alignment, only used via pointers
extern fn lib_open() ?*Handle;
extern fn lib_close(h: *Handle) void;

const Iface = struct {
    ptr: *anyopaque,
    vtable: *const VTable,
    const VTable = struct { speak: *const fn (*anyopaque) void };
    fn speak(self: Iface) void { self.vtable.speak(self.ptr); }
};
fn dogSpeak(p: *anyopaque) void {
    const d: *Dog = @ptrCast(@alignCast(p));
    d.bark();
}
```
- `std.mem.Allocator` itself is this pattern (`ptr: *anyopaque`, `vtable: *const VTable`); read its source for a reference implementation.
- `opaque {}` can contain declarations like structs, unions and enums: `const Db = opaque { pub fn close(self: *Db) void { ... } };`. It is typically used for type safety with C code that hides struct details.
- `void` has size 0; `anyopaque` has an unknown but non-zero size.
- Prefer tagged unions (closed sets) or `anytype` (comptime generics) before vtables.

## Gotchas
- Keep the vtable and the object created together in one constructor so the `@ptrCast` target always matches the real type.
- `@alignCast` is the builtin to raise a pointer's alignment after a cast from `*anyopaque`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the `opaque` and `void` sections and the `@alignCast` text of the language reference; the `ptr`/`vtable` fields of `std.mem.Allocator`. Removed: the unchecked-`@ptrCast` and alignment-1 claims.

Method: documentation only; no commands were run.

## Self-check
Implement two structs behind `Iface`, call both through the vtable, and confirm alignment casts pass under Debug.
