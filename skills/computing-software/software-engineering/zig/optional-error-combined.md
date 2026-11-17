---
id: computing-software.software-engineering.zig.optional-error-combined
name: optional-error-combined
category: computing-software
field: software-engineering
product: zig
tags: [zig, optional-error-combined, zig-optionals, error-union-optional, nullable-pointer, iterator-next]
level: practitioner
status: docs-checked
description: "Combine ?T and error unions (!?T, ?!T), optional pointers and iterator patterns correctly in Zig, with unwrapping order."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref.html.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optionals combined with error unions and pointers
**Goal:** pick the right nesting and unwrap it cleanly.

- `!?T` (error or optional): "failed, or ok-but-nothing". Typical for `next()` on iterators that can fail: `fn next(self: *It) !?Item`.
```zig
while (try it.next()) |item| { ... }     // try handles the error, capture handles null
const v = (try lookup(k)) orelse return error.Missing;
const n = (try parse(s)) orelse 0;
```
- `try` is a prefix operator (grammar: `PrefixExpr <- PrefixOp* PrimaryExpr`) and binds tighter than the binary `orelse`, so `try x orelse y` is `(try x) orelse y`; parenthesise when in doubt.
- Pointer to optional payload: `if (opt) |*p| p.* += 1;`; `opt.?` is the unwrap that asserts non-null.
- `orelse` with a struct literal: `const cfg = maybe_cfg orelse Config{};`.

## Gotchas
- Unwrap the error union with `try`/`catch` before using `.?` or `orelse` on the optional inside it.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Optionals section and the grammar (`PrefixExpr`, `orelse` in the binary operator table) of the language reference. Fixed: `try x orelse y` is `(try x) orelse y`, not `try (x orelse y)`. Removed: pointer-size, `?!T` and `.?` rules (unchecked).

Method: documentation only; no commands were run.

## Self-check
Write an iterator over lines returning `!?[]const u8` and loop with `while (try it.next()) |l|`.
