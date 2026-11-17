---
id: computing-software.game-programming.game-engine-architecture.parallel-for-patterns
name: parallel-for-patterns
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, parallel-for-loop, job-system, data-parallelism, game-programming]
level: practitioner
status: draft
description: "Write parallel-for loops on a job system: batch sizing, contiguous ranges, reductions without contention, write-disjoint outputs and avoiding tiny jobs."
sources: ["https://docs.unity3d.com/ScriptReference/Unity.Jobs.IJobParallelFor.html", "https://github.com/oneapi-src/oneTBB"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parallel-for patterns

**Goal:** spread a loop over N items across worker threads with near-linear scaling.

## Shape
```cpp
void parallelFor(size_t n, size_t batch, auto&& body) {   // body(begin, end)
    size_t jobs = (n + batch - 1) / batch;
    Counter c{jobs};
    for (size_t j = 0; j < jobs; ++j)
        js.submit([=, &c] { body(j * batch, std::min(n, (j + 1) * batch)); c.dec(); });
    js.waitAndHelp(c);    // caller executes jobs while waiting, never just blocks
}
```
Equivalent APIs: Unity `IJobParallelFor.Schedule(length, innerloopBatchCount)` (or
`IJobFor.ScheduleParallel`), TBB `parallel_for(blocked_range)`, C++17 `std::for_each(std::execution::par, ...)`.

## Batch size
- Each job should take roughly 20-200 microseconds; tiny jobs drown in scheduling overhead.
- Batch = max(minBatch, n / (workers * 4)) gives load balancing slack for uneven work.
- Uneven per-item cost (AI agents with varied work) favours smaller batches or work stealing.

## Data rules
- Each item writes only its own output slot (write-disjoint); reads of shared data are read-only.
- Contiguous ranges per job avoid false sharing on outputs.
- Reductions: per-job partial results in padded slots, combine after the loop. Never an atomic
  increment per item.
- Appending to a shared list: per-job local lists then concatenate, or atomic index reservation in
  blocks.

## Pitfalls
- Spawning a parallel-for from inside a job and blocking: the worker must help-execute, or deadlock.
- Structural changes (spawn/destroy) inside the loop: record into per-job command buffers.
- Loops over a few hundred cheap items are faster serial.

## Verify
- Scaling test at 1, 2, 4, 8 workers; profile shows balanced lanes and small idle gaps.
- Run under ThreadSanitizer.
