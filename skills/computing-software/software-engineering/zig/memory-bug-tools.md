---
id: computing-software.software-engineering.zig.memory-bug-tools
name: memory-bug-tools
category: computing-software
field: software-engineering
product: zig
tags: [zig, memory-bug-tools, zig-debugging, valgrind, leak-detection, use-after-free, tsan, gpa-leak]
level: advanced
status: draft
description: "Locate leaks, use-after-free and races in Zig with the debug allocator, std.testing.allocator, valgrind and thread sanitizer."
sources:
  - https://zig.guide/
  - https://ziglang.org/documentation/master/std/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding memory bugs: GPA leak reports, valgrind, sanitizers
**Goal:** catch memory errors early.

- Use the debug allocator (`GeneralPurposeAllocator` or `DebugAllocator`) in Debug builds and check `deinit()` result; it records allocation stack traces and reports leaks and double-free with traces.
- `std.testing.allocator` does the same in tests.
- `.safety`, `.stack_trace_frames`, `.verbose_log` options on the GPA config; set `stack_trace_frames` > 0 for readable leak traces (default depends on build mode).
- Valgrind (Linux): `valgrind --leak-check=full ./app` works on Zig binaries; combine with `c_allocator` (libc malloc) so valgrind sees real allocations: the Zig-native allocators use `mmap` directly, so valgrind may miss internal bugs (partial support via client requests, unconfirmed).
- Thread sanitizer: `-fsanitize-thread` flag on build (support varies; unconfirmed).
- Address sanitizer for linked C code: `-fsanitize=address` in C flags via `addCSourceFiles` and linking libasan (platform specific; unconfirmed).
- Poison on free: Debug builds set freed memory to `0xaa` patterns, making use-after-free show recognizable garbage.
- Write tests with `FailingAllocator` and `checkAllAllocationFailures` for error-path leaks.

## Gotchas
- Arena allocators hide per-allocation leaks until the whole arena is not deinitialised.
- `std.process.exit` and `@panic` skip `defer gpa.deinit()`, so no leak report.

## Self-check
Leak one allocation intentionally, run a Debug build, and read the leak trace file:line.
