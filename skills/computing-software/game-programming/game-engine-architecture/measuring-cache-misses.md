---
id: computing-software.game-programming.game-engine-architecture.measuring-cache-misses
name: measuring-cache-misses
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, cache-miss-profiling, profiling, data-oriented-design, game-programming]
level: practitioner
status: draft
description: "Measure cache behaviour in engine code: perf and VTune memory analysis, cache-miss counters, Cachegrind, interpreting results and confirming DOD changes."
sources: ["https://perf.wiki.kernel.org/index.php/Tutorial", "https://valgrind.org/docs/manual/cg-manual.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring cache misses

**Goal:** prove that a system is memory-bound and that a data-layout change actually helped.

## Tools
- **perf (Linux):** `perf stat -e cycles,instructions,cache-references,cache-misses,L1-dcache-load-misses,LLC-load-misses ./game --bench`.
  `perf record -e mem_load_retired.l3_miss:pp` (Intel) then `perf report` attributes misses to lines.
- **Intel VTune:** Microarchitecture Exploration / Memory Access analysis shows "Memory Bound"
  share and which data structures miss.
- **AMD uProf:** cache analysis with IBS sampling.
- **Cachegrind** (`valgrind --tool=cachegrind`): simulated, slow, deterministic; good for comparing
  two implementations offline.
- **Superluminal/Tracy** for timing; pair with counters to explain timing.
- Consoles: platform profilers (Razor, PIX) expose hardware counters.

## Reading results
- Low IPC (instructions per cycle, under ~1 on a modern core) with high LLC misses = memory-bound.
- High L1 misses but low LLC misses: working set fits L2/L3; layout tweaks give smaller wins.
- Hot spots on pointer-chasing (`node = node->next`, `entity->component->data`) indicate AoS or
  linked structures; convert to contiguous arrays (SoA) and iterate linearly.

## Method
1. Make a repeatable benchmark (fixed scene, fixed frame count, pinned CPU frequency if possible).
2. Measure counters before.
3. Change layout (SoA, hot/cold split, sort by access).
4. Measure counters after; check both miss counts and wall time.

## Pitfalls
- Sampling skid: attributed line may be after the actual load.
- Virtual machines often hide hardware counters.
- Turbo boost and thermal throttling noise; run several iterations.

## Verify
- Record a before/after table (cycles, IPC, LLC misses, ms) for the change in the PR.
