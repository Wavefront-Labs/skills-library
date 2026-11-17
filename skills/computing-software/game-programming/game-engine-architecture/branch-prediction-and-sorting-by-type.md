---
id: computing-software.game-programming.game-engine-architecture.branch-prediction-and-sorting-by-type
name: branch-prediction-and-sorting-by-type
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, branch-prediction, data-oriented-design, sorting, game-programming]
level: practitioner
status: draft
description: "Reduce branch mispredictions in hot loops: sort or bucket entities by type, branchless selects, avoiding virtual calls per element, and measuring with counters."
sources: ["https://gameprogrammingpatterns.com/data-locality.html", "https://www.agner.org/optimize/microarchitecture.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Branch prediction and sorting by type

**Goal:** hot loops over thousands of entities that don't stall on unpredictable branches.

## Cost
A mispredicted branch costs roughly 15-20 cycles on modern x86 (Agner Fog's microarchitecture
guide). A loop doing `if (e.active)` or a virtual call over randomly mixed types can mispredict
half the time.

## Techniques
1. **Sort or bucket by type/state:** keep active and inactive objects in separate arrays (Nystrom's
   *Data Locality* pattern: move active particles to the front so the loop needs no `if`). In ECS,
   archetypes do this naturally: different component sets live in different chunks.
2. **Process per type, not per object:** instead of `for e: e->update()` with virtual dispatch over
   mixed types, iterate one array per type. Removes indirect branch mispredictions and improves
   I-cache use.
3. **Sort draw/update lists** by material, mesh or behaviour so consecutive elements take the same path.
4. **Branchless code** for simple selects:
   ```cpp
   x = cond ? a : b;           // often compiles to cmov/blend
   mask = -(int)(v > limit); v = (v & ~mask) | (limit & mask);
   ```
   SIMD code uses masks and blends throughout. Don't hand-write branchless code where the branch
   is predictable; it can be slower.
5. **Hoist invariant branches** out of loops (separate loops per mode).

## Measuring
- Linux `perf stat -e branches,branch-misses ./bench`; VTune "Bad Speculation"; AMD uProf.
- Microbenchmark sorted vs shuffled inputs to see the effect.

## Verify
- Branch-miss rate in the hot system drops after bucketing; frame time improves in the profiler,
  not just the microbenchmark.
