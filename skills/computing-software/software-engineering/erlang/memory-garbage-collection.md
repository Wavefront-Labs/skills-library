---
id: computing-software.software-engineering.erlang.memory-garbage-collection
name: memory-garbage-collection
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-vm, memory-garbage-collection]
level: sme
status: draft
description: "BEAM memory: per-process generational GC, fullsweep_after, hibernate, refc binaries, sub-binary leaks and erlang:memory."
sources:
  - https://www.erlang.org/doc/apps/erts/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Memory, garbage collection and binaries
**Goal:** reason about memory use and fix leaks.

- Each process has its own heap collected independently with a generational copying collector; `fullsweep_after` (spawn option and `+hmax`-style limits) controls promotion.
- Binaries over 64 bytes live in a shared reference-counted area; processes hold references, so a leak shows as growing binary memory with small process heaps.
- Fixes: `binary:copy/1` for retained pieces, `erlang:garbage_collect/0` on long-lived processes, `hibernate` for idle servers (`{noreply, S, hibernate}`).
- `erlang:memory()` shows totals by area; `recon_alloc:memory(allocated)` vs `used` shows fragmentation.
- `erlang:process_info(Pid, [memory, heap_size, total_heap_size, binary])` per process.
- Limit blast radius with `max_heap_size`.
```erlang
spawn_opt(fun worker/0, [{fullsweep_after, 10}, {min_heap_size, 4096}]).
```

## Gotchas
- Setting `fullsweep_after` to 0 makes every GC a full sweep and burns CPU.

## Self-check
Create a retained sub-binary leak, observe with `recon:bin_leak/1`, then fix it with `binary:copy/1`.
