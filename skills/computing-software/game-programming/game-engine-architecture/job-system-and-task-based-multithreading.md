---
id: computing-software.game-programming.game-engine-architecture.job-system-and-task-based-multithreading
name: job-system-and-task-based-multithreading
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, job-system, task-graph, multithreading, work-stealing, thread-pool, fiber, dependency-graph, false-sharing, data-race, lock-free, frame-graph, parallel-for, game-programming]
level: sme
status: draft
description: "Architect an engine's parallelism as a job graph with explicit dependencies and a work-stealing scheduler, instead of one fixed thread per subsystem."
sources: ["https://www.gdcvault.com/play/1022186/Parallelizing-the-Naughty-Dog-Engine", "https://blog.molecular-matters.com/2015/08/24/job-system-2-0-lock-free-work-stealing-part-1/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Job system and task-based multithreading architecture

**Goal:** the engine-wide design decision underneath a specific API like
Unity's Job System — why modern engines model all parallel work as a graph of
small jobs with explicit dependencies on a shared worker pool, instead of
"the render thread," "the physics thread," "the audio thread" as fixed,
separately-managed threads.

## Why "one thread per subsystem" stopped scaling
The old model (a render thread, a physics thread, a game logic thread,
hand-synchronized with mutexes/semaphores between them) hits two walls: it
caps parallelism at the number of subsystems regardless of core count (8
subsystems can't use 16 cores), and load imbalance is constant — the physics
thread sits idle while the render thread is the bottleneck this frame, and
vice versa next frame, with no way to borrow idle capacity. The job-graph model
(popularized publicly by Naughty Dog's talks on the Uncharted/Last of Us
engine, and the basis of Unity's Job System, Unreal's Task Graph) instead has
a **fixed pool of worker threads** (typically = core count) and breaks all
work — rendering, physics, animation, gameplay — into small **jobs**, each
declaring what it depends on. A scheduler runs any job whose dependencies are
satisfied on any free worker, so the whole core count is kept busy regardless
of which subsystem currently has more work.

## Work-stealing: the scheduling algorithm that makes it fair
Each worker thread has its own local job queue (push/pop from the thread that
owns it — no contention for the common case) plus the ability to **steal**
from the back of another thread's queue when its own is empty. This keeps
load balanced without a central lock being hit on every job dequeue (a naive
single shared queue becomes the bottleneck itself past a handful of threads).
Jobs should be sized to make stealing worthwhile — a job that takes 2
microseconds costs more in scheduling overhead than it saves; batch tiny work
into one job (e.g. "update these 500 particles" as one job, not 500 one-particle
jobs).

## Dependencies are the real design problem
The graph's edges (job B can't start until job A finishes) are what prevent
races, but authoring them wrong causes either a **deadlock** (a dependency
cycle — A waits on B, B waits on A) or a **silent race** (a missing dependency
means B reads data A hasn't finished writing, intermittent and
hardware/timing-dependent, the worst class of bug to reproduce). Safety
systems that check this at runtime (Unity's Job Safety System throwing on
undeclared reads) exist precisely because manual dependency bookkeeping is
error-prone at any real scale — if your engine doesn't have one, the design
cost is on you to get every dependency declared and no "I'll just read it,
it's probably done by now."

## What NOT to parallelize
- Anything whose job overhead exceeds its work (see sizing above).
- Work with heavy false sharing — multiple jobs writing to adjacent memory
  (different fields of the same cache line) serialize at the cache-coherency
  level even with zero logical dependency; pad/separate hot per-job data to
  cache-line boundaries (typically 64 bytes) when this shows up in a profiler
  as unexplained contention.
- Anything requiring a specific OS thread (some platform APIs, certain audio/
  input callbacks must run on a designated thread) — these stay as fixed
  threads outside the job pool by necessity, not by default.

## Verify
- [ ] Worker thread count is tied to actual core count (with headroom for OS/
      other processes), not a hardcoded number from a different target platform.
- [ ] Every job's declared dependencies are verified against what it actually
      reads/writes — ideally enforced by a safety system, not code review alone.
- [ ] Profiler (a timeline/trace view, not just total CPU%) shows worker
      utilization reasonably even across a representative frame, not a few
      threads busy and others idle.
- [ ] No job's measured execution time is smaller than the scheduler's
      measured per-job overhead; tiny work is batched.
