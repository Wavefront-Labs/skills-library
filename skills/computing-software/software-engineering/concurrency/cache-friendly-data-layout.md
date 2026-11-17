---
id: computing-software.software-engineering.concurrency.cache-friendly-data-layout
name: cache-friendly-data-layout
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, optimisation, cache-friendly, data-oriented-design, struct-of-arrays, memory-locality, false-sharing]
level: practitioner
status: draft
description: "Speed up hot loops with cache-friendly data layout: arrays of structs vs structs of arrays, contiguous storage, field ordering, avoiding pointer chasing and false sharing."
sources:
  - https://www.dataorienteddesign.com/dodbook/
  - https://www.akkadia.org/drepper/cpumemory.pdf
  - https://perf.wiki.kernel.org/index.php/Tutorial
  - https://easyperf.net/notes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cache-friendly data layout

Memory access, not arithmetic, dominates most hot loops. Rough latencies: L1 ~1 ns, L2 ~4 ns, L3 ~10-20 ns, DRAM ~80-100 ns. A cache line is 64 bytes on x86 and most ARM (128 bytes on Apple M-series for some levels); the hardware prefetcher rewards sequential access.

## Principles
1. **Contiguous over linked:** arrays/vectors beat linked lists and trees of heap nodes for iteration. A `std::vector`/`ArrayList<int>`-equivalent primitive array/`[]T` scans at memory bandwidth; a linked list costs a cache miss per node.
2. **Touch only what you need:** if a loop reads 2 fields of a 200-byte object, most of each cache line is wasted.
3. **Sequential and predictable access** lets the prefetcher hide latency; random access defeats it.

## AoS vs SoA
```c
// Array of Structs: good when you use most fields of each element together
struct Particle { float x, y, z, vx, vy, vz; uint32_t color; char name[32]; };
struct Particle ps[N];

// Struct of Arrays: good when hot loops use a few fields across all elements
struct Particles { float *x, *y, *z, *vx, *vy, *vz; };
for (size_t i = 0; i < n; i++) { p.x[i] += p.vx[i] * dt; }   // dense, vectorisable
```
Hybrid: split hot fields from cold ones (hot/cold splitting) - keep `position, velocity` in one array, rarely used `name, metadata` elsewhere. ECS game engines (Unity DOTS, Bevy, EnTT) are built on this.

## Managed languages
- Java: arrays of objects are arrays of pointers to scattered objects; use primitive arrays (`double[]`) or parallel arrays for hot data; Project Valhalla value classes will help. JOL (`org.openjdk.jol`) shows object layout and padding.
- C#: `struct` arrays are contiguous; `Span<T>`, `ArrayPool<T>`; avoid boxing.
- Python: lists hold pointers to boxed objects; use NumPy arrays (contiguous, typed) or `array` module for numeric data; columnar formats (Arrow, Polars) for tables.
- Go: slices of structs are contiguous; slices of pointers are not.

## Field ordering and padding
Order struct fields largest to smallest to reduce padding (C/C++/Go/Rust `#[repr(C)]`; Rust reorders by default). Tools: `pahole` (C), `go vet -fieldalignment` (via `fieldalignment` analyzer), `-Wpadded`.

## False sharing
Two threads writing different variables on the same cache line ping-pong the line between cores. Pad or align per-thread counters to 64/128 bytes (`alignas(64)`, Java `@Contended` with `-XX:-RestrictContended`, Go padding arrays, `crossbeam_utils::CachePadded`), or accumulate per thread and combine at the end.

## Measure
```bash
perf stat -e cycles,instructions,cache-references,cache-misses,L1-dcache-load-misses ./bench
perf c2c record ./app && perf c2c report        # false sharing detection
valgrind --tool=cachegrind ./bench
```
Intel VTune memory access analysis, AMD uProf. Compare before/after with a benchmark harness, not a single run.

## Verify
- [ ] Benchmark shows the speedup at realistic data sizes (larger than L3, not just toy sizes).
- [ ] Cache-miss counters drop correspondingly; profile confirms the loop was hot to begin with.
