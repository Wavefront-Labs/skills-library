---
id: computing-software.software-engineering.zig.tagged-unions
name: tagged-unions
category: computing-software
field: software-engineering
product: zig
tags: [zig, tagged-unions, zig-enums-unions, union-enum, tagged-union, activetag, payload-capture]
level: practitioner
status: docs-checked
description: "Build Zig tagged unions (union(enum)), switch with payload captures, mutate payloads by pointer, and use them for variant data."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tagged unions and payload captures
**Goal:** safe variants instead of C unions.

```zig
const Value = union(enum) {
    int: i64,
    float: f64,
    text: []const u8,
    nil,                                  // void payload
    pub fn isNum(v: Value) bool {
        return switch (v) { .int, .float => true, else => false };
    }
};
var v: Value = .{ .int = 5 };
switch (v) {
    .int => |*i| i.* += 1,
    .text => |t| std.debug.print("{s}\n", .{t}),
    else => {},
}
if (v == .int) {}                         // compare tag
const tag = std.meta.activeTag(v);
```
- Accessing the wrong field (`v.float` when `.int` is active) panics in safe modes (illegal behavior otherwise).
- `union(enum)` auto-generates the tag enum; `union(MyEnum)` uses an existing one; a bare `union { }` is untagged (no safety, Debug adds a hidden tag).
- `extern union` / `packed union` for C and bit layouts.
- Tagged union + `inline else` handles every case generically.
- Constructing void-payload members: `.nil`; others `.{ .int = 1 }`.

## Gotchas
- Changing the active field must assign the whole union: `v = .{ .float = 1.0 };`.
- Payload pointer captures `|*x|` are invalid after reassigning the union.

## Self-check
Build an expression tree union (num, add) and evaluate it recursively using `*const Expr` children.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: union(enum), union(Tag), untagged unions, payload captures (language reference unions section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
