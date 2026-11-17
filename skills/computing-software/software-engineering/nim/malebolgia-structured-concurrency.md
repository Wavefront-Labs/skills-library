---
id: computing-software.software-engineering.nim.malebolgia-structured-concurrency
name: malebolgia-structured-concurrency
category: computing-software
field: software-engineering
product: nim
tags: [malebolgia-structured-concurrency, threads-and-parallelism, malebolgia, taskpools, weave, structured-concurrency, master, awaitall, nimble, nim]
level: sme
status: docs-checked
description: "Use the malebolgia library for structured fork-join with createMaster, spawn and awaitAll, with cancellation, timeouts and lockers."
sources:
  - https://github.com/Araq/malebolgia
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Malebolgia and structured parallelism

Goal: use a small structured-parallelism library.

- Pattern:
```nim
import malebolgia
var m = createMaster()
m.awaitAll:
  for i in 0 ..< n:
    m.spawn work(i) -> results[i]
```
- `awaitAll` is a barrier: it waits for every spawned task, which is what makes the concurrency structured. There are no `FlowVar`s; `spawn f(x) -> sums[i]` stores the result and the barrier synchronizes, so no `sync` is needed.
- Goals and features from the README: only structured concurrency, bounded memory use (backpressure as a side effect), detection of simple read/write and write/write conflicts, built-in cancellation and timeouts, under 300 lines with no dependencies.
- Tuning: compile with `-d:ThreadPoolSize=8 -d:FixedChanSize=16`. `ThreadPoolSize` is usually the number of CPU cores (higher for IO-bound programs); the default `FixedChanSize` is usually good enough.
- Exceptions: if a spawned task raises, the master rethrows after `awaitAll`; with several failures only the first is kept.
- Cancellation: `m.cancel()`. Timeouts: `createMaster(initDuration(milliseconds=500))`; on expiry cancellation is requested and `awaitAll` waits for all tasks before raising the timeout error. Long tasks should poll `m.cancelled`.
- `Master` cannot be passed to subroutines; `getHandle(m)` gives a `MasterHandle` that can `spawn` and cancel but not `awaitAll`.
- Shared data: wrap in `Locker[T]` from `malebolgia/lockers` (`lock results as r:` and `unprotected results as r:`), or pass `addr` of an outer variable together with a `TicketLock` from `malebolgia/ticketlocks`.

Gotchas:
- `var T` parameters are not supported for spawned procs; pass a pointer to a variable declared outside the `awaitAll` block.
- Unprotected shared mutation from several tasks is a data race; protect with a lock.

Verify: the results array is fully populated after the `awaitAll` block.

## Checked

2026-11-08. Read in full: the malebolgia README (Araq/malebolgia). Removed: the `nimble install malebolgia` line, taskpools and weave comparisons, the ORC/ARC and `Isolated` claim, and the `--threads:on -d:release` advice (none in the README); manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
