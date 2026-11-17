---
id: computing-software.software-engineering.zig.process-args-env
name: process-args-env
category: computing-software
field: software-engineering
product: zig
tags: [zig, process-args-env, zig-std-process, argsalloc, argiterator, getenvvarowned, std-process]
level: practitioner
status: docs-checked
description: "Read command-line args and environment variables in Zig with std.process.args, argsAlloc, getEnvVarOwned and ArgIterator."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/process.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/process/Child.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command-line arguments and environment variables
**Goal:** parse program inputs.

```zig
const args = try std.process.argsAlloc(alloc);
defer std.process.argsFree(alloc, args);
if (args.len < 2) { std.debug.print("usage: {s} <file>\n", .{args[0]}); std.process.exit(2); }

var it = try std.process.argsWithAllocator(alloc);   // portable iterator
defer it.deinit();
_ = it.skip();
while (it.next()) |a| { ... }

const home = std.process.getEnvVarOwned(alloc, "HOME") catch |e| switch (e) {
    error.EnvironmentVariableNotFound => null,
    else => return e,
};
```
- `args[0]` is the program name. `argsWithAllocator` is the cross-platform iterator (documented).
- `std.process.getEnvMap(alloc)` returns all variables.
- Exit status: `std.process.exit(code)` skips defers; return `!void` from main for normal flow (error exits with 1).
- Child processes: `std.process.Child.run(.{ .allocator = alloc, .argv = &.{ "git", "status" } })` returns `.stdout`, `.stderr`, `.term` (free the buffers); lower level `std.process.Child.init` with `spawn`/`wait`.

## Gotchas
- `exit` does not run deferred cleanup nor leak checks.
- Env var values are borrowed or owned depending on function; check the name (`Owned`).
- Never build shell strings from input; use argv arrays.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `argsAlloc`/`argsFree`, `argsWithAllocator` (cross-platform note), `ArgIterator.skip`, `getEnvVarOwned`, `error.EnvironmentVariableNotFound`, `getEnvMap`, `exit`, `Child.run`. Removed: the zig-clap bullet and the Windows `args()` remark.

Method: documentation only; no commands were run.

## Self-check
Write a tool that prints each arg and the value of `PATH` length; run `Child.run` on `zig version` and print stdout.
