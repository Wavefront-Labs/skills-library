---
id: computing-software.software-engineering.d.d-std-parallelism-taskpool
name: d-std-parallelism-taskpool
category: computing-software
field: software-engineering
product: d
tags: [d-std-parallelism-taskpool, concurrency-parallelism, std-parallelism, parallel-foreach, taskpool, task, amap, reduce, workunitsize, data-parallelism, d]
level: practitioner
status: docs-checked
description: "Parallelise loops and tasks using std.parallelism: parallel(), task(), taskPool.map/reduce/amap, workUnitSize, scoped tasks, totalCPUs and avoiding races."
sources:
  - https://dlang.org/phobos/std_parallelism.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.parallelism: parallel foreach, task, taskPool, parallel map/reduce

Goal: speed up CPU-bound loops safely.

```d
import std.parallelism, std.range;
foreach (i; parallel(iota(n), 100)) out[i] = heavy(i);    // 100 = work unit size
auto total = taskPool.reduce!"a + b"(0.0, taskPool.map!f(data));
auto t = task!compute(args); t.executeInNewThread(); auto r = t.yieldForce;
```
- `parallel(range, workUnitSize)` for foreach; smaller work units balance load better, larger ones cut the overhead of fetching work. Each iteration must write distinct data and not share mutable state.
- `taskPool.map!f(range, bufSize)` (lazy), `taskPool.amap` (eager), `taskPool.reduce`, `asyncBuf`, `workerLocalStorage` (for example `workerLocalStorage(0.0L)` for per-thread accumulators).
- `task!f(args)` creates a task; run it with `taskPool.put(t)` or `executeInNewThread()`; `yieldForce` returns the result (rethrowing any exception the task threw); `scopedTask` stays on the stack.
- Default worker count is `totalCPUs - 1`; `defaultPoolThreads(n)` sets it, but calling it after the first use of `taskPool` does not change the existing pool.

Gotchas:
- `break`, labeled `break`/`continue`, `return` or `goto` out of a parallel foreach throws `ParallelForeachError`.
- When a loop body throws, submission of further work stops and already queued work units complete before the exception is rethrown.

Verify: compare timing against the serial loop with `StopWatch` and check identical results.

## Checked

2026-11-03. Confirmed against: std.parallelism reference page (parallel foreach, map/amap/reduce, asyncBuf, workerLocalStorage, task, scopedTask, yieldForce, defaultPoolThreads, exception handling).

Removed because the pages read did not confirm it: the `shared`/`atomicOp` bullet and the `taskPool.put` run recipe wording; gotcha about uncaught throws replaced by the documented exception behaviour.

Method: documentation only; no commands were run.
