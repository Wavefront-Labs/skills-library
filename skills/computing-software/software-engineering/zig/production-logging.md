---
id: computing-software.software-engineering.zig.production-logging
name: production-logging
category: computing-software
field: software-engineering
product: zig
tags: [zig, production-logging, zig-deployment, log-level, signal-handling, graceful-shutdown, version-embedding, runtime-config]
level: practitioner
status: draft
description: "Configure Zig std.log for production, embed version info, read config from env and files, and handle signals and graceful shutdown."
sources:
  - https://ziglang.org/documentation/master/std/
  - https://zig.guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logging, versioning and runtime configuration in production
**Goal:** make a Zig service operable.

- Logging: set `std_options.log_level` and a custom `logFn` writing structured lines (timestamp, level, scope) to stderr or a file; compile-time level (`log_level`) removes lower levels; runtime filtering via `log_scope_levels`.
- Embed version: `b.addOptions()` with git hash/version (see build options skills), print on `--version`.
- Config: env vars (`std.process.getEnvVarOwned`), a JSON/ZON file parsed at startup, flags via CLI; validate and fail fast.
- Signals (POSIX):
```zig
var stop = std.atomic.Value(bool).init(false);
fn onSig(_: c_int) callconv(.C) void { stop.store(true, .release); }
const act = std.posix.Sigaction{ .handler = .{ .handler = onSig }, .mask = std.posix.empty_sigset, .flags = 0 };
std.posix.sigaction(std.posix.SIG.INT, &act, null);
std.posix.sigaction(std.posix.SIG.TERM, &act, null);
while (!stop.load(.acquire)) { ... }
```
  (`std.posix.sigaction` return type and handler union shape vary by release; unconfirmed.)
- On Windows use `SetConsoleCtrlHandler` via `std.os.windows` bindings.
- Use ReleaseSafe in production; ship unstripped symbols separately for crash analysis.
- Health endpoints and metrics are your own responsibility (no built-in framework).

## Gotchas
- Signal handlers may only do async-signal-safe things: set an atomic flag, nothing else.
- Logging from multiple threads interleaves unless you lock stderr (`std.debug.lockStdErr`).

## Self-check
Start a loop, send SIGTERM, and confirm it exits cleanly with buffers flushed.
