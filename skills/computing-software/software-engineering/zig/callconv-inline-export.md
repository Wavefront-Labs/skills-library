---
id: computing-software.software-engineering.zig.callconv-inline-export
name: callconv-inline-export
category: computing-software
field: software-engineering
product: zig
tags: [zig, callconv-inline-export, zig-functions, callconv, inline-fn, noinline, export-fn]
level: advanced
status: docs-checked
description: "Control inlining, symbol export and calling convention on Zig functions with inline, noinline, export, extern and callconv."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref/export_builtin.zig
  - https://github.com/ziglang/zig/blob/0.15.1/doc/langref/test_functions.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# inline, noinline, export and calling conventions
**Goal:** control codegen and linkage deliberately.

```zig
inline fn fast(x: u32) u32 { return x * 2; }        // forces inlining (use sparingly)
noinline fn cold() void {}                           // prevents inlining
export fn zig_add(a: c_int, b: c_int) c_int { return a + b; }   // C symbol, C ABI
extern fn puts(s: [*:0]const u8) c_int;              // declared elsewhere, needs libc linked
fn cb(x: c_int) callconv(.c) void { _ = x; }         // C-ABI callback
```
- `export` makes a C-ABI, externally visible symbol; params and returns must be extern-compatible types (C ints, pointers, extern structs).
- In 0.15.1 the calling convention is spelled `.c` (`callconv(.c)` in the language reference examples); Windows API functions use `.winapi`.
- `inline fn` makes the function semantically inlined at the call site, not an optimizer hint: comptime-known arguments become comptime parameters, so it changes types and values. Use it sparingly.
- Call-site control: `@call(modifier, function, args)` with `std.builtin.CallModifier` (it has `always_inline` and `never_inline`).
- Use `pub fn main` normally.

## Gotchas
- Use the `@export` builtin (or the `export` keyword) to make a symbol visible to other objects; the language reference's `export_builtin.zig` shows `@export` with an internal function name.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `callconv(.c)` and `.winapi` in the language reference examples, the `inline fn` section, `@call` and `CallModifier` (`always_inline`, `never_inline` in builtin.zig), and the `export`/`@export` text. Fixed: `callconv(.C)` in the example is `callconv(.c)` in 0.15.1. Removed: rename history, `main` linking and generic-export claims.

Method: documentation only; no commands were run.

## Self-check
Build a static library with an `export fn`, run `nm`/`dumpbin` and see the symbol; call it from a C file.
