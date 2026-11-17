---
id: computing-software.game-programming.game-engine-architecture.memory-budgets-and-tracking
name: memory-budgets-and-tracking
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, memory-allocators, memory-budget, memory-tracking, allocation-tags, leak-detection, memory-profiler, platform-memory, game-programming, memory-leak-detection]
level: practitioner
status: draft
description: "Set and enforce per-system memory budgets: tagging allocations, tracking high-water marks, leak detection by snapshot diff, and budget reports in CI and soak tests."
sources: ["https://www.gameenginebook.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-low-level-memory-tracker-in-unreal-engine", "https://docs.unity3d.com/Packages/com.unity.memoryprofiler@1.1/manual/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory budgets and tracking

**Goal:** every system knows its memory budget on each target platform, and the build tells you
who blew it before QA does.

## 1. Define budgets
Start from the platform's usable memory for the title (minus OS/reserved), then allocate by system:
| System | Example share |
|---|---|
| Textures/streaming pool | 35-45% |
| Meshes/animation | 10-15% |
| Audio | 5-10% |
| Gameplay/simulation | 5-10% |
| Physics/navigation | 5% |
| UI | 3-5% |
| Engine/code/stack/misc | remainder + 10% headroom |
Write it down per platform and per mode (menu, largest level, multiplayer).

## 2. Tag allocations
- Route all allocations through engine allocators that take a **tag** (scope-based):
  `MEM_SCOPE(Tag::Physics);` pushes a thread-local tag used by the allocator.
- Track per tag: current bytes, peak bytes, allocation count. Overhead: a header or a side table keyed
  by address.
- Catch third-party allocations by overriding their allocator hooks (most middleware takes callbacks).
- Unreal: **LLM** (Low Level Memory tracker) tags: run with `-llm`, view with `stat llm` /
  `stat llmfull`, `-llmcsv` to write CSVs. `memreport -full` for a text snapshot.
- Unity: Memory Profiler package snapshots (categories: native, managed, graphics, untracked);
  `Profiler.GetTotalAllocatedMemoryLong()`; ProfilerRecorder for counters at runtime.

## 3. Watch high-water marks, not averages
OOM happens at peaks: level transitions (old and new level both resident), cinematics, streaming
bursts. Log peak per tag per level.

## 4. Leak detection
- Snapshot at the same point twice (menu, after loading and unloading a level); diff by tag and by
  callstack. Growth = leak or cache without a cap.
- Debug builds: record callstack per allocation (sampled if too slow); report allocations still alive
  at shutdown.

## 5. Enforce
- Automated run per nightly build: load each level, record peaks to CSV, fail or warn when a tag
  exceeds budget; trend graph over builds.
- In-game overlay showing budget bars per tag (red when over) for content creators.
- Texture/asset budgets enforced at import/cook time (sizes, mip counts) are cheaper than runtime fixes.

## Verify
- [ ] Every allocation is attributed (untracked/"misc" < 5% of total).
- [ ] Nightly report shows per-level peak vs budget for each platform.
- [ ] Menu -> level -> menu snapshot diff shows no growth beyond known caches.
