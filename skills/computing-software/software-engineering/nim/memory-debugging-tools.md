---
id: computing-software.software-engineering.nim.memory-debugging-tools
name: memory-debugging-tools
category: computing-software
field: software-engineering
product: nim
tags: [memory-debugging-tools, memory-management, valgrind, asan, sanitizer, usemalloc, leak, memory-profile, nimallocstats, nim]
level: advanced
status: docs-checked
description: "Find leaks and corruption with -d:useMalloc, valgrind, AddressSanitizer, and Nim's own allocation statistics."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/mm.html
  - https://nim-lang.org/docs/system.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory debugging: valgrind, sanitizers, useMalloc

Goal: verify memory behaviour.

- `-d:useMalloc` makes Nim use C's `malloc` instead of its own memory manager; it only works with `--mm:none`, `--mm:arc` and `--mm:orc`. The memory-management comparison table marks ARC, ORC, YRC and atomic ARC as Valgrind compatible and refc, markAndSweep, boehm and go as not.
- So for Valgrind or a C sanitizer build with `nim c -d:useMalloc --mm:orc prog.nim`; pass sanitizer flags to the C compiler with `--passC:` and `--passL:`.
- In-program stats: `getOccupiedMem()`, `getFreeMem()`, `getTotalMem()`; `GC_getStatistics()` returns a string of GC statistics (not on every memory manager).
- `--debugger:native` enables `--debuginfo --lineDir:on` for use with GDB, LLDB or CDB.
- Allocation profiling: the embedded profiler's memory mode (see the benchmarking skill, `-d:memProfiler`).

Gotchas:
- With `--mm:arc` a cyclic structure leaks, which a leak checker reports.

Verify: a deliberate leak of a `ref` cycle under `--mm:arc -d:useMalloc` shows up in the leak checker.

## Checked

2026-11-02. Confirmed against nimc.md (`useMalloc`), mm.md (compatibility table, ARC leaks cycles), intern.md (`--debugger:native`) and lib/system/memalloc.nim and gc_interface.nim (stat procs). Removed: the valgrind and `-fsanitize` command lines (external tools), `memTracker` and `nimTypeNames` (only seen in allocator source, not in docs), the ASan-threads and reachable-memory gotchas.
Method: documentation only; no commands were run.
