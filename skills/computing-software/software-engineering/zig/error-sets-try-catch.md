---
id: computing-software.software-engineering.zig.error-sets-try-catch
name: error-sets-try-catch
category: computing-software
field: software-engineering
product: zig
tags: [zig, error-sets-try-catch, zig-errors, error-union, try, catch, inferred-error-set, anyerror]
level: practitioner
status: docs-checked
description: "Define Zig error sets, return error unions, propagate with try, handle with catch and switch on errors, and infer error sets."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error sets, error unions, try and catch
**Goal:** model failure as values.

```zig
const FileError = error{ NotFound, Denied };
fn open(path: []const u8) FileError!File { ... }
fn run() !void {                              // inferred error set
    const f = try open("a");                  // propagate on error
    const g = open("b") catch |err| switch (err) {
        error.NotFound => return error.Missing,
        error.Denied => @panic("denied"),
    };
    const h = open("c") catch default_file;   // fallback value
    _ = .{ f, g, h };
}
```
- `try x` is `x catch |e| return e`. An error set is a set of names; the same name in different sets is the same value.
- Merge sets with `||`: `A || B`. `anyerror` is the superset (loses precision; avoid in library APIs).
- Inferred sets (`!T`) are convenient but make recursive functions and function pointers need explicit sets.
- `@errorName(err)` gives the string; `std.log.err("{s}", .{@errorName(e)})`.
- `error.Foo` can be returned directly: `return error.Foo;`.
- `catch unreachable` asserts no error (UB when wrong in unsafe modes).
- `main` may be `pub fn main() !void`; a returned error prints a trace and exits non-zero.

## Gotchas
- Errors carry no payload. Return diagnostics via an out-parameter struct (`diag: *?Diagnostic`) or tagged union.
- You must handle or propagate every error union: discarding is a compile error ("error union is ignored"). Use `_ = f() catch {};` deliberately.

## Self-check
Write a function returning `error{Neg}!u32`, test with `std.testing.expectError(error.Neg, f(-1))`.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: error sets, merge with ||, anyerror, try/catch, catch unreachable, error unions must be handled (language reference errors section).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
