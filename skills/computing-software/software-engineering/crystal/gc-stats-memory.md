---
id: computing-software.software-engineering.crystal.gc-stats-memory
name: gc-stats-memory
category: computing-software
field: software-engineering
product: crystal
tags: [gc-stats-memory, gc-runtime, gc-stats, gc-collect, gc-disable, memory-leak, heap-size, rss, gc-profile-stats, allocation-profile, crystal]
level: advanced
status: draft
description: "Use the GC module: GC.stats, GC.collect, GC.disable, profile stats and diagnose leaks and high memory use."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GC stats, manual collection and memory diagnosis

Goal: diagnose memory.

- `GC.stats` returns `heap_size`, `free_bytes`, `unmapped_bytes`, `bytes_since_gc`, `total_bytes`; `GC.prof_stats` more detail.
- `GC.collect` forces a collection; `GC.disable` / `GC.enable` pause it around latency-critical sections.
- Leak hunting: print `GC.stats` periodically; look for growing global collections (Hash caches without eviction, Array of fibers, Channel buffers, `at_exit` handlers).
- Fibers hold stacks; thousands of blocked fibers cost memory.
- Release builds with `--no-debug` reduce binary size, not heap.

Gotchas:
- RSS lags heap_size because freed pages are not returned immediately.
- `GC.collect` in loops hurts throughput.
- Weak references are not in stdlib; use ids and a registry.

Verify: `GC.stats.heap_size` stabilises under steady load.
