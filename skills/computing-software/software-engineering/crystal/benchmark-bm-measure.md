---
id: computing-software.software-engineering.crystal.benchmark-bm-measure
name: benchmark-bm-measure
category: computing-software
field: software-engineering
product: crystal
tags: [benchmark-bm-measure, benchmark, benchmark-bm, time-measure, profiling, perf, valgrind, flamegraph, allocation, memory-usage, crystal]
level: advanced
status: draft
description: "Use Benchmark.bm and Time.measure for one-shot timings, plus perf, valgrind and --stats for deeper profiling."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmark.bm, Time.measure and profiling

Goal: find hot spots.

- `Benchmark.bm { |x| x.report("sort") { arr.sort } }` prints user/system/total/real times; `Benchmark.realtime { }` returns a Span; `Time.measure { }` too.
- Profile native binaries with `perf record -g ./app` then `perf report` / flamegraph; debug info is kept in release builds unless `--no-debug`.
- Memory: `GC.stats` (heap_size, total_bytes), `valgrind` is noisy with Boehm GC; use `heaptrack` where available.
- Reduce allocations: use `String.build`, `IO::Memory`, avoid intermediate `Array`s with `each` and iterators, prefer structs and `Slice`.
- `crystal build --release --stats` shows compile cost; `--no-debug` shrinks binary.

Gotchas:
- Boxed closures and unions allocate; check with `GC.stats` before/after.
- Single-run timings are unreliable; repeat.
- Optimise only measured bottlenecks.

Verify: before/after `ips` shows a gain.
