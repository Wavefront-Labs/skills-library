---
id: computing-software.game-programming.game-engine-architecture.false-sharing-and-cache-line-contention
name: false-sharing-and-cache-line-contention
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, cache-line-contention, false-sharing, multithreading, game-programming]
level: practitioner
status: draft
description: "Find and fix false sharing: threads writing variables on the same cache line, padding to 64 bytes, per-thread accumulators and detecting it with perf c2c."
sources: ["https://en.cppreference.com/w/cpp/thread/hardware_destructive_interference_size", "https://man7.org/linux/man-pages/man1/perf-c2c.1.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# False sharing

**Goal:** stop threads slowing each other down by writing different variables that share a cache line.

## Mechanism
Caches move data in 64-byte lines (128 on Apple M-series for some purposes). If thread A writes
`counters[0]` and thread B writes `counters[1]` on the same line, the line bounces between cores
(MESI invalidations) even though no data is actually shared. Throughput can drop several times.

## Typical game-engine cases
- Per-worker job counters/stats in an array of ints.
- Job system queue head and tail indices in one struct.
- Parallel-for writing results into adjacent small elements (writing bools per entity from
  different threads in interleaved order).
- Atomic flags next to frequently-read data.

## Fixes
```cpp
struct alignas(std::hardware_destructive_interference_size) PaddedCounter { std::atomic<uint64_t> v; };
PaddedCounter perWorker[kMaxWorkers];
```
- `std::hardware_destructive_interference_size` (C++17; may warn about ABI; many engines just use 64).
- Accumulate in thread-local variables and combine once at the end.
- Partition parallel-for work into contiguous chunks (index ranges) rather than interleaved indices.
- Separate producer-written and consumer-written fields of lock-free queues onto different lines.

## Detecting
- Linux: `perf c2c record ./game` then `perf c2c report` shows cache lines with HITM (modified
  hits) and the offsets/threads involved.
- Intel VTune Memory Access analysis; AMD uProf.
- Symptom: scaling gets worse as threads are added on a workload with no real sharing.

## Verify
- Benchmark per-worker counters with and without padding at 8+ threads; the padded version should
  scale nearly linearly.
