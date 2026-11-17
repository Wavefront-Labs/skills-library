---
id: computing-software.software-engineering.zig.debugger-gdb-lldb
name: debugger-gdb-lldb
category: computing-software
field: software-engineering
product: zig
tags: [zig, debugger-gdb-lldb, zig-debugging, gdb, lldb, debug-info, breakpoints, zig-test-exe]
level: practitioner
status: draft
description: "Debug Zig executables in Debug mode using gdb, lldb or editor debug adapters, with symbol names, breakpoints and test binaries."
sources:
  - https://zig.guide/
  - https://ziglang.org/learn/build-system/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging Zig programs with gdb, lldb and the VS Code debugger
**Goal:** step through Zig code.

- Debug mode emits DWARF (PDB on Windows MSVC ABI); do not pass `-fstrip` or `.strip = true` while debugging.
```bash
zig build                             # Debug by default
gdb --args zig-out/bin/app arg1
(gdb) break main.main                 # symbol names are file.function: e.g. main.main, std.heap.arena_allocator.ArenaAllocator.alloc
(gdb) run
(gdb) bt
(gdb) info locals
lldb zig-out/bin/app
(lldb) b main.zig:12
```
- Debug a failing test: build the test exe without running it: `zig test src/x.zig --test-no-exec -femit-bin=./t` or, in build.zig, `b.installArtifact(unit)`, then debug `./t`.
- For a build run step use `zig build run -- ...` after installing the artifact; or run the installed binary directly.
- Pretty printers for Zig types are limited; use `print`/`p` with explicit fields, or `std.debug.print` for complex values.
- VS Code: use CodeLLDB or C/C++ debug adapters with a `launch.json` pointing to the binary; names of extensions evolve (unconfirmed).

## Gotchas
- Optimised release builds inline and reorder; debug in Debug mode first, then ReleaseSafe with debug info (`strip = false`).
- `undefined` shows as `0xaa` in Debug memory.

## Self-check
Set a breakpoint in a function, print a local, and get a backtrace of two frames.
