---
id: computing-software.data-engineering.prefect.background-tasks
name: background-tasks
category: computing-software
field: data-engineering
product: prefect
tags: [background-tasks, delay, task-worker, serve, map]
level: practitioner
status: docs-checked
description: "Run Prefect tasks in the background with task.delay, task.serve, prefect.task_worker.serve and deferred map submission."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/run-background-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: queue task runs for a separate worker process.

Define the task normally with `@task` (optionally `log_prints=True`).

Start a worker for one task:

```python
add.serve()
```

From another process queue a run; `.delay()` takes the same signature as the function:

```python
add.delay(1, 2)
```

One worker for several tasks:

```python
from prefect.task_worker import serve
serve(add, multiply)
```

Tasks queued with `.delay()` run once a worker starts.

Batches: submit many runs without running them, then start a worker.

```python
from prefect import unmapped
add.map(A, B, deferred=True)
add.map(A, unmapped(4), deferred=True)   # keep one argument fixed
add.serve()
```

`.map()` accepts iterables of positional arguments, iterables of kwargs, or `unmapped` inputs.

The guide does not cover CLI commands, environment variables or limits. Further examples are in the prefect-background-task-examples repository it links to.

## Checked
2026-11-08. Confirmed against the background tasks how-to: task.serve(), task.delay() signature, prefect.task_worker.serve for several tasks, map with deferred=True and unmapped, and the Iterable argument forms. Nothing removed.
Method: documentation only; no commands were run.
