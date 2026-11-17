---
id: computing-software.software-engineering.zig.errdefer-traces
name: errdefer-traces
category: computing-software
field: software-engineering
product: zig
tags: [zig, errdefer-traces, zig-errors, errdefer, error-return-trace, errorreturntrace]
level: advanced
status: docs-checked
description: "Clean up on failure with errdefer, read Zig error return traces, and keep traces useful through catch and rethrow."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# errdefer and error return traces
**Goal:** release partial state on error paths and debug where errors originate.

```zig
fn create(a: std.mem.Allocator) !*Thing {
    const t = try a.create(Thing);
    errdefer a.destroy(t);              // runs only if we return an error
    t.buf = try a.alloc(u8, 1024);      // if this fails, t is destroyed
    errdefer a.free(t.buf);
    try t.init();
    return t;
}
```
- `defer` always runs at scope exit; `errdefer` only on error return; both run in reverse order.
- `errdefer |err| log(err);` captures the error.
- Error return traces (Debug and ReleaseSafe) record every `return error.X` / `try` site, printed when an error escapes `main`. They are not stack traces of the current stack; they show the path the error took.
- `catch |e| return e` keeps the trace; `catch return error.Other` starts a new origin and loses it.
- `@errorReturnTrace()` returns `?*std.builtin.StackTrace`; `std.debug.dumpStackTrace`.

## Gotchas
- Traces are disabled in ReleaseFast/Small and may be off with `-fstrip`.
- Do not `errdefer` after the final success statement expecting it to cover later code; it applies only to returns after the declaration.

## Self-check
Make `t.init()` fail, run under `std.testing.allocator`, and confirm no leak report because errdefer freed both allocations.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: errdefer, error return traces, @errorReturnTrace (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
