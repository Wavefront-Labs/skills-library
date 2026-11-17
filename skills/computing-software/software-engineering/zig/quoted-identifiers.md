---
id: computing-software.software-engineering.zig.quoted-identifiers
name: quoted-identifiers
category: computing-software
field: software-engineering
product: zig
tags: [zig, quoted-identifiers, zig-lexical, at-quoted, identifier-rules, discard-underscore]
level: intro
status: docs-checked
description: "Use Zig identifier rules, @\"...\" quoted names, and the _ discard to handle keywords, odd field names and unused values."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identifiers and @"quoted" names
**Goal:** name things legally and know how to escape reserved words.

## Rules
- Identifiers start with a letter or `_`, then letters, digits, `_`. Keywords (`fn`, `error`, `type`, `test`, ...) are reserved.
- Escape anything else with `@"..."`: `const @"error" = 1;`, `const @"my field" = 2;`. Commonly used for C/JSON field names that collide with keywords.
- `_` is a write-only discard: `_ = value;` silences "unused" errors. It is not a variable and cannot be read.
- Primitive type names (`u8`, `i32`, `f64`, `bool`, `usize`, `void`, `type`, `anyerror`, `noreturn`) are identifiers that cannot be shadowed. Arbitrary-width ints like `u7` or `i129` are also primitive type names (u1 to u65535).

```zig
const std = @import("std");
const Msg = struct { @"type": []const u8, id: u32 };
pub fn main() void {
    const m = Msg{ .@"type" = "ping", .id = 1 };
    std.debug.print("{s} {d}\n", .{ m.@"type", m.id });
    const unused = 5;
    _ = unused;
}
```

## Gotchas
- Unused local variables, parameters and (since early versions) unused function arguments are compile errors; discard with `_ = x;`.
- Unused top-level declarations are not errors, only lazily analysed: a broken unused `fn` compiles fine until referenced.
- Shadowing an outer-scope name with a local is an error in Zig ("local shadows declaration").

## Self-check
Declare `const fn = 1;` (fails), then `@"fn"` (passes). Declare an unused local and observe the error; add `_ = x;` to fix.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: @"..." identifiers, shadowing error, arbitrary-width integer names (language reference).
- Removed or changed: the unsourced claim about how a variable named u8 is lexed.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
