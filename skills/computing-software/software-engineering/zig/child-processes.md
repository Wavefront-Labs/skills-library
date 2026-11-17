---
id: computing-software.software-engineering.zig.child-processes
name: child-processes
category: computing-software
field: software-engineering
product: zig
tags: [zig, child-processes, zig-std-process, process-child, spawn, argv, term-exited, stdout-capture]
level: practitioner
status: docs-checked
description: "Spawn and wait for child processes in Zig with std.process.Child.run, stdio behaviors, environment and exit-code handling."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/process/Child.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/process.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running child processes and capturing output
**Goal:** call external tools safely.

```zig
const res = try std.process.Child.run(.{
    .allocator = alloc,
    .argv = &.{ "git", "rev-parse", "HEAD" },
    .max_output_bytes = 1 << 20,
});
defer alloc.free(res.stdout);
defer alloc.free(res.stderr);
switch (res.term) {
    .Exited => |code| if (code != 0) return error.CommandFailed,
    else => return error.CommandCrashed,
}

var child = std.process.Child.init(&.{"cat"}, alloc);
child.stdin_behavior = .Pipe;
child.stdout_behavior = .Pipe;
try child.spawn();
try child.stdin.?.writeAll("hi");
child.stdin.?.close();
child.stdin = null;
const out = try child.stdout.?.readToEndAlloc(alloc, 1 << 16);
const term = try child.wait();
```
- `Child.run` options (0.15.1): `allocator`, `argv`, `cwd`, `cwd_dir`, `env_map`, `max_output_bytes` (default 50 * 1024), `expand_arg0`, `progress_node`. It runs with stdin ignored and stdout/stderr piped.
- `Child.init(argv, allocator)` defaults `stdin_behavior` to `.Inherit`; `stdin_behavior`, `stdout_behavior` and `stderr_behavior` take `.Inherit`, `.Ignore` or `.Pipe`; `cwd` and `env_map` are fields.
- `Term` variants: `Exited: u8`, `Signal: u32`, `Stopped: u32`, `Unknown: u32`.
- `argv` is a list of arguments passed directly, with no shell involved.
- `std.process.execv(allocator, argv)` replaces the current process.
- `Child.collectOutput` exists for reading stdout and stderr of a spawned child.

## Self-check
Run `zig version` through `Child.run` and compare stdout with the compiler's version.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/process/Child.zig` (`run`, `init`, `Term`, `collectOutput`, `spawn`, `wait`) and `lib/std/process.zig` (`execv`); `File.readToEndAlloc` in `lib/std/fs/File.zig`.
Removed: deadlock claim for sequential pipe reads, shell-via-`sh -c` advice, "fields reorganised in 0.14-0.15" hedge, leak gotcha.
Method: documentation only; no commands were run.
