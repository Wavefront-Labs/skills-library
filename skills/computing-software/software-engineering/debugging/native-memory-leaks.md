---
id: computing-software.software-engineering.debugging.native-memory-leaks
name: native-memory-leaks
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, memory-debugging, memory-leaks, leaksanitizer, heaptrack, valgrind, massif, jemalloc-profiling, rss-growth, fragmentation, memory-fragmentation, jemalloc]
level: advanced
status: docs-checked
description: "Find native (C/C++/Rust/C-extension) memory leaks and growth: LeakSanitizer, Valgrind memcheck/massif, heaptrack and jemalloc profiling, plus telling leaks from fragmentation."
sources: ["https://clang.llvm.org/docs/LeakSanitizer.html", "https://valgrind.org/docs/manual/mc-manual.html", "https://valgrind.org/docs/manual/ms-manual.html", "https://github.com/KDE/heaptrack", "https://github.com/jemalloc/jemalloc/wiki/Use-Case%3A-Heap-Profiling"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Native memory leaks

**Goal:** explain why a native process's RSS keeps growing, and find the allocation
site responsible.

## 1. Leak or something else?
RSS growth can be: true leak (unreachable allocations), unbounded caches/queues
(reachable but growing), allocator fragmentation/retention (freed memory not returned
to the OS), or memory-mapped files. Check the process memory maps under `/proc/<pid>/` (anonymous vs file-backed)
and your allocator's own statistics (see the allocator's documentation).

## 2. In tests: LeakSanitizer
```bash
clang -fsanitize=address -g ...      # LSan is included with ASan on Linux
ASAN_OPTIONS=detect_leaks=1 ./tests  # report at exit with allocation stacks
LSAN_OPTIONS=suppressions=lsan.supp  # suppress known third-party leaks
```
Run the test suite under ASan in CI: catches leaks at the PR that introduces them.

## 3. Unmodified binaries: Valgrind
```bash
valgrind --leak-check=full --show-leak-kinds=definite,indirect --track-origins=yes ./app
valgrind --tool=massif ./app && ms_print massif.out.<pid>     # heap over time, peak snapshot tree
```
Large slowdown; use on a reproduction, not production.

## 4. Long-running processes: heaptrack / jemalloc
```bash
heaptrack ./app            # can also attach to an already running process (see its README)
heaptrack --analyze /tmp/heaptrack.app.<pid>.gz    # reports include temporary allocations
```
Aimed at longer runs than Valgrind. With jemalloc:
`MALLOC_CONF=prof:true,lg_prof_interval:30,prof_prefix:/tmp/jeprof` then
`jeprof --svg app /tmp/jeprof.*.heap` and compare successive dumps (`--base`).

## Language bindings
Python/Node/Ruby native extensions leak outside the managed heap: managed heap
snapshots look flat while RSS grows. Use heaptrack/jemalloc on the interpreter process.

## Fragmentation fixes
Allocators can keep freed memory resident (per-thread arenas, decay delays), which looks like a leak.
To tell fragmentation from a leak, compare allocator-reported in-use memory with RSS, try
a different allocator or its documented trim/decay tuning options (look them up in that allocator's
docs; not confirmed here), and test RSS over hours.

## Verify
- [ ] Leak site identified with an allocation stack and fixed; ASan/LSan test added.
- [ ] RSS flat over a soak test of several hours at production-like load.

## Checked

2026-11-02. Confirmed from the LeakSanitizer page (ASan integrates and enables LSan by default; -fsanitize=leak; LSAN_OPTIONS suppressions), Valgrind Memcheck and Massif manuals (--leak-check, --show-leak-kinds, --track-origins, ms_print), the heaptrack README (attach to a running process, .gz output, temporary allocations) and the jemalloc heap-profiling wiki (prof:true, prof_prefix, lg_prof_interval, jeprof --base). Removed or generalised because no fetched source states them: /proc smaps_rollup and glibc malloc_stats/malloc_info, the 20-50x Valgrind slowdown figure, the heaptrack .zst file name and GUI description, the Rust jemalloc/dhat advice, and the MALLOC_ARENA_MAX / malloc_trim / jemalloc decay and stats details.

Method: documentation only; no commands were run.
