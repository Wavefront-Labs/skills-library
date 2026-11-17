---
id: computing-software.software-engineering.ruby.ruby-gc-tuning
name: ruby-gc-tuning
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, gc-tuning, memory]
level: advanced
status: draft
description: "Inspect and tune the Ruby GC with GC.stat, RUBY_GC_* variables and ObjectSpace, and tell leaks from bloat."
sources: ["https://docs.ruby-lang.org/en/master/GC.html", "https://docs.ruby-lang.org/en/master/ObjectSpace.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Garbage collector tuning

Look before tuning:
```ruby
GC.stat                       # hash: count, major_gc_count, heap_live_slots, total_allocated_objects...
GC.stat(:total_allocated_objects)
GC.start; GC.compact          # compaction is available in 3.x; test before production
require "objspace"
ObjectSpace.count_objects     # live objects by type
ObjectSpace.memsize_of(obj)
ObjectSpace.trace_object_allocations { ... }   # then ObjectSpace.allocation_sourcefile(obj)
```
Environment variables (names from the Ruby GC docs; defaults differ by version, check `GC.config` / docs for yours): `RUBY_GC_HEAP_INIT_SLOTS`, `RUBY_GC_HEAP_GROWTH_FACTOR`, `RUBY_GC_MALLOC_LIMIT`, `RUBY_GC_OLDMALLOC_LIMIT`. Setting a larger initial heap reduces startup GC runs for boot-heavy apps.

## Method
1. Record `GC.stat[:count]` and allocations around the suspect request (`GC.stat` before/after, or the `memory_profiler` gem).
2. Reduce allocations first (frozen strings, `each` not `map` chains, `String#<<`), which pays more than any knob.
3. Leaks vs bloat: if `heap_live_slots` grows steadily after full GCs, objects are retained (caches, globals, closures); if RSS grows but live slots do not, suspect malloc fragmentation and try `MALLOC_ARENA_MAX=2` or jemalloc.

## Gotchas
- `GC.disable` in production only postpones the cost and can exhaust memory.
- Forking servers rely on copy-on-write; call `GC.compact` or `GC.start` before fork in preload mode (Puma, Unicorn) and measure RSS per worker.
- Tuning without a load test is guessing.

Verify: compare `GC.stat(:major_gc_count)` and p99 latency under the same load before and after each single change.
