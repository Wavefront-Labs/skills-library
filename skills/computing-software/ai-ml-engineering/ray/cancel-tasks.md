---
id: computing-software.ai-ml-engineering.ray.cancel-tasks
name: cancel-tasks
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-cancel, task-cancel, force-cancel, taskcancellederror]
level: practitioner
status: docs-checked
description: "Cancel running or pending Ray tasks with ray.cancel (graceful vs force, recursive) and handle TaskCancelledError."
sources:
  - https://docs.ray.io/en/latest/ray-core/tasks.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.cancel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancelling tasks

```python
@ray.remote
def slow():
    time.sleep(600)

ref = slow.remote()
ray.cancel(ref)                       # sends KeyboardInterrupt to the task (graceful)
ray.cancel(ref, force=True)           # kills the worker process
ray.cancel(ref, recursive=True)       # also cancel child tasks it launched (default True)

try:
    ray.get(ref)
except ray.exceptions.TaskCancelledError:
    print("cancelled")
```
`ray.get` raises `TaskCancelledError` even with `force=True` (not `WorkerCrashedError`). Actor tasks: a pending call is cancelled; a running call on a regular or threaded actor only gets a cancellation flag you can poll with `ray.get_runtime_context().is_canceled()`; an async actor's `asyncio.Task` is cancelled. `force=True` on an actor task raises `ValueError`; use `ray.kill(actor)` instead.

## Gotchas
- A pending task is cancelled without executing; with `force=False` a running task gets a `KeyboardInterrupt`, with `force=True` the worker is killed.
- Cancelled tasks are not retried, and `max_task_retries` is not respected.
- Cancelling an already finished task does nothing.
- With `recursive=True` and `force=True`, `force` is ignored for child actor tasks.

## Verify
`ray.get(ref)` raises `TaskCancelledError` quickly.

## Checked
2026-11-03: checked against the `ray.cancel` docstring in `python/ray/_private/worker.py` and the Ray docs source `core/fault-tolerance/tasks.md`, `core/tasks/index.md`. Fixed: force-cancel raises `TaskCancelledError`, not `WorkerCrashedError`; actor task cancel semantics. Removed the unsourced bytecode-boundary, lost-results and Data/Serve claims and the `ray list tasks` filter.
Method: documentation only; no commands were run.
