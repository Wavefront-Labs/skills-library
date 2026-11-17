---
id: computing-software.software-engineering.zig.profiling-benchmark
name: profiling-benchmark
category: computing-software
field: software-engineering
product: zig
tags: [zig, profiling-benchmark, zig-performance, perf, callgrind, benchmark, donotoptimizeaway, assembly-output]
level: advanced
status: draft
description: "Benchmark Zig code with std.time.Timer and doNotOptimizeAway, profile with perf, Instruments or valgrind callgrind, and inspect assembly."
sources:
  - https://zig.guide/
  - https://ziglang.org/documentation/master/std/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmarking and profiling Zig programs
**Goal:** measure, then optimise.

```zig
var timer = try std.time.Timer.start();
var acc: u64 = 0;
for (0..iterations) |i| {
    acc +%= work(i);
    std.mem.doNotOptimizeAway(acc);
}
const ns = timer.read();
std.debug.print("{d} ns/iter\n", .{ns / iterations});
```
- Build for benchmarks with `-Doptimize=ReleaseFast` and `strip = false` so profilers can name functions.
- Linux `perf record -g ./app; perf report`; `perf stat` for IPC/cache misses.
- macOS Instruments Time Profiler; Windows: Visual Studio profiler or `xperf`.
- `valgrind --tool=callgrind` and `kcachegrind` for call-graph profiles.
- Assembly: `zig build-exe src/main.zig -O ReleaseFast -femit-asm=main.s` (flag per `zig build-exe --help`; unconfirmed) or use objdump on the binary.
- Common wins: avoid allocations in loops (reuse buffers), struct-of-arrays (`MultiArrayList`), SIMD `@Vector`, `comptime` specialisation, buffered IO.
- Run several iterations, discard warmup, use median.

## Gotchas
- The optimizer can delete a loop whose result is unused; sink results with `doNotOptimizeAway`.
- Frame pointers may be omitted in release; add `-fno-omit-frame-pointer` (C flag) or `.omit_frame_pointer = false` (module option; unconfirmed) for readable `perf` stacks.

## Self-check
Benchmark two implementations of a sum and confirm the winner is consistent over five runs.
