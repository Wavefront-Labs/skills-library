---
id: computing-software.software-engineering.zig.error-diagnostics
name: error-diagnostics
category: computing-software
field: software-engineering
product: zig
tags: [zig, error-diagnostics, zig-errors, diagnostic-struct, error-context, error-mapping, result-union]
level: advanced
status: docs-checked
description: "Carry context with Zig errors using diagnostic out-parameters, tagged result unions and error mapping, since errors have no payload."
sources:
  - https://ziglang.org/documentation/0.15.1/#Errors
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/json/Scanner.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/zon/parse.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error payloads and diagnostics patterns
**Goal:** useful error messages without exceptions.

Zig errors are bare names. A common way to add context is an optional out-parameter:
```zig
pub const Diagnostic = struct { line: usize = 0, col: usize = 0, msg: []const u8 = "" };
pub fn parse(src: []const u8, diag: ?*Diagnostic) error{Syntax}!Ast {
    ...
    if (bad) {
        if (diag) |d| d.* = .{ .line = l, .col = c, .msg = "unexpected token" };
        return error.Syntax;
    }
}
```
- The standard library uses this shape: `std.json` has `Diagnostics` in `Scanner.zig` and `std.zon` has `Diagnostics` in `zon/parse.zig`.
- Error sets are merged with `||` (`(A || B) == error{One, Two}`).
- Use static messages in the diagnostic so it has no allocation lifetime to manage.

## Self-check
Parse bad input and print `line:col: message` from the diagnostic while returning `error.Syntax`.

## Checked
2026-11-02. Confirmed in `lib/std/json/Scanner.zig` and `lib/std/zon/parse.zig` (`pub const Diagnostics`) and the 0.15.1 language reference (error set merging).
Removed: tagged-union result alternative, layer-mapping switch example, logging-at-boundary advice, `else => |e| return e` and `unreachable` advice, exit-code advice, `anyerror` gotcha, "names unconfirmed" hedge.
Method: documentation only; no commands were run.
