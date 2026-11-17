---
id: computing-software.software-engineering.nim.benchmarking-and-profiling
name: benchmarking-and-profiling
category: computing-software
field: software-engineering
product: nim
tags: [benchmarking-and-profiling, build-optimization-flags, benchmark, profiling, perf, callgrind, nimprof, benchy, flamegraph, performance, nim]
level: advanced
status: docs-checked
description: "Measure performance with monotimes and benchy, profile with perf, valgrind callgrind and Nim's embedded profiler."
sources:
  - https://nim-lang.org/docs/estp.html
  - https://nim-lang.org/docs/monotimes.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Benchmarking and profiling Nim programs

Goal: find and verify speedups.

- Time in code with `std/monotimes` (`getMonoTime()`; `ticks` gives an `int64`).
- Benchmark release builds: `-d:release` turns on the optimizer, `-d:danger` also turns off runtime checks; `--debuginfo:on` adds debug information. External profilers (perf, valgrind) work on the produced binary but their flags are not covered by Nim's docs.
- Embedded Stack Trace Profiler (CPU): compile with `--profiler:on --stackTrace:on`, `import std/nimprof` (for example under `when compileOption("profiler")`); the program writes `profile_results.txt` when it finishes.
- Memory profiler: compile with `--profiler:off --stackTrace:on -d:memProfiler` (yes, `--profiler:off`) and import `nimprof`; define `ignoreAllocationSize` to count allocations only.

Gotchas:
- The profiler needs `--stackTrace:on`, so a profiling build is much slower than a release build.

Verify: the profile results file lists the hot proc and later runs show improvement.

## Checked

2026-11-02. Confirmed against estp.md (flags, `nimprof`, `profile_results.txt`, memory profiler, `ignoreAllocationSize`), lib/std/monotimes.nim (`getMonoTime`, `ticks`), nimc.md and advopt.txt. Fixed: the memory profiler uses `--profiler:off`, not `--profiler:on`. Removed: benchy, perf and valgrind command lines, `-fno-omit-frame-pointer`, the optimisation tips list, the debug-build and dead-code gotchas.
Method: documentation only; no commands were run.
