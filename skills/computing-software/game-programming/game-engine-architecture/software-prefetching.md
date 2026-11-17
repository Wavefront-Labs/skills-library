---
id: computing-software.game-programming.game-engine-architecture.software-prefetching
name: software-prefetching
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, prefetching, data-oriented-design, cache, game-programming]
level: practitioner
status: draft
description: "Use software prefetch intrinsics where hardware prefetchers fail: prefetch distance, pointer-chasing and indirect access patterns, and when it hurts."
sources: ["https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html", "https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Software prefetching

**Goal:** hide memory latency for access patterns the hardware prefetcher can't predict.

## When hardware already does it
Linear scans and constant strides are detected automatically. Software prefetching on those
usually adds instructions for no gain. Target:
- Indirect access: `data[indices[i]]` (gather by index lists, sparse sets).
- Pointer chasing where the next address is known early (linked lists of known nodes, tree traversal
  where children are known).
- Hash table lookups in batches.

## Intrinsics
```cpp
#include <xmmintrin.h>
for (size_t i = 0; i < n; ++i) {
    if (i + D < n) _mm_prefetch((const char*)&data[indices[i + D]], _MM_HINT_T0);
    process(data[indices[i]]);
}
// GCC/Clang portable: __builtin_prefetch(addr, /*rw*/0, /*locality*/3);
```
- `_MM_HINT_T0` all cache levels, `T1`/`T2` outer levels, `NTA` non-temporal (streaming data used once).
- Prefetch distance D: enough iterations to cover memory latency (~100 ns) divided by work per
  iteration. Tune empirically (try 4, 8, 16, 32).
- ARM: `__builtin_prefetch` maps to `PRFM`.

## Batch lookups
Process lookups in groups: compute addresses for a batch of 8-16 keys, prefetch all, then
process all. This overlaps misses (memory-level parallelism).

## When it hurts
- Too far ahead: lines evicted before use. Too many: pollutes cache and consumes bandwidth.
- On memory-bandwidth-bound loops it changes nothing.

## Verify
- Benchmark with and without; check LLC misses and time with perf/VTune. Keep only prefetches that
  measurably win on target hardware (console CPUs differ from dev PCs).
