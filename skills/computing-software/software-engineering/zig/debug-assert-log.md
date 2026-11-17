---
id: computing-software.software-engineering.zig.debug-assert-log
name: debug-assert-log
category: computing-software
field: software-engineering
product: zig
tags: [zig, debug-assert-log, zig-std-math-meta, std-debug, std-log, assert, scoped-log, std-options]
level: practitioner
status: docs-checked
description: "Use std.debug.print, assert, panic, stack traces and std.log scoped logging with custom log levels and handlers in Zig."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/debug.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/log.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/std.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.debug, assertions and std.log
**Goal:** structured diagnostics and invariants.

```zig
std.debug.print("x = {d}\n", .{x});                 // stderr, always on
std.debug.assert(len > 0);                           // checked in Debug/ReleaseSafe only
if (bad) @panic("invariant broken");
std.debug.dumpCurrentStackTrace(@returnAddress());   // print where we are

const log = std.log.scoped(.net);
log.info("connected to {s}", .{host});
log.err("failed: {s}", .{@errorName(e)});

pub const std_options: std.Options = .{ .log_level = .debug, .logFn = myLog };   // in root file
```
- `std.log` levels: err, warn, info, debug; default compile-time level depends on build mode (`.debug` in Debug, `.info` in ReleaseSafe/Fast/Small).
- `std.debug.assert(false)` is `unreachable`: in ReleaseFast it is an optimisation hint, not a check. For release-time checks return errors or `@panic`.
- Use `@src()` for function/line info; `std.debug.lockStdErr()` around multiple prints in threads.

## Gotchas
- `std.debug.print` writes to stderr and silently returns on failure; it is meant for printf debugging, with `std.log` for proper logging.
- `assert` with side effects disappears in release-fast.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `debug.print` (stderr, silent on failure), `assert` (`if (!ok) unreachable`), `panic`, `lockStdErr`, `dumpCurrentStackTrace(start_addr)`, `log.scoped`, `log.default_level` by build mode, and the `std_options: std.Options` example in log.zig. Removed: the pre-0.14 `std_options` boundary claim.

Method: documentation only; no commands were run.

## Self-check
Override `logFn` to prefix timestamps and verify a scoped log line prints with `[net]`.
