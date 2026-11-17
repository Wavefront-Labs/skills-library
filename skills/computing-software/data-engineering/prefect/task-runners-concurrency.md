---
id: computing-software.data-engineering.prefect.task-runners-concurrency
name: task-runners-concurrency
category: computing-software
field: data-engineering
product: prefect
tags: [task-runner, threadpool, futures, processpool, map]
level: practitioner
status: docs-checked
description: "Run Prefect tasks concurrently with ThreadPoolTaskRunner, ProcessPoolTaskRunner, Dask or Ray, resolve futures and avoid child-task deadlocks."
sources:
  - https://docs.prefect.io/v3/concepts/task-runners
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and configure a task runner.

Task runners are optional: calling a task directly runs it in the main thread and blocks. Use `.submit()` or `.map()` to send tasks to a runner.

| Runner | Model |
|---|---|
| `ThreadPoolTaskRunner` | default, threads |
| `ProcessPoolTaskRunner` | `multiprocessing`, CPU-bound |
| `DaskTaskRunner` | `prefect[dask]` |
| `RayTaskRunner` | `prefect[ray]` |

```python
@flow(task_runner=ThreadPoolTaskRunner(max_workers=3))
```
`ProcessPoolTaskRunner` also takes `initializer` and `initargs` (called once per worker subprocess before any task).

Futures: `.submit()` returns a `PrefectFuture`. A future passed to a downstream task makes Prefect wait; the task receives the value. `.result()` blocks and raises on failure; `raise_on_failure=False` returns the exception, then check `future.state.is_failed()`.

Futures must be resolved before a flow or task returns: return them, call `.wait()` or `.result()`, or use top-level `wait` or `as_completed`.

Considerations: too many small tasks add overhead; `.map` can exceed resources; pass references not large data; thread runner needs thread-safe globals, Dask and Ray need picklable globals.

Deadlock: a bounded thread pool whose threads are all parents blocked on `.result()` of children. Fix with `max_workers` above nesting depth or `PREFECT_TASKS_RUNNER_THREAD_POOL_MAX_WORKERS=N`, submit children at flow level, or use `.delay()`.

## Checked
2026-11-08. Confirmed against the Task runners concept page: the four runners and extras, max_workers, ProcessPoolTaskRunner initializer and initargs, PrefectFuture resolution rules, result() and raise_on_failure, design considerations and the bounded thread pool deadlock fixes including PREFECT_TASKS_RUNNER_THREAD_POOL_MAX_WORKERS. Nothing removed.
Method: documentation only; no commands were run.
