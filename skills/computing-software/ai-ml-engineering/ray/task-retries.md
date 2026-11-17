---
id: computing-software.ai-ml-engineering.ray.task-retries
name: task-retries
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, max-retries, retry-exceptions, task-fault-tolerance, lineage-reconstruction]
level: practitioner
status: docs-checked
description: "Configure Ray task fault tolerance: max_retries for worker crashes, retry_exceptions for app errors, and object lineage reconstruction."
sources:
  - https://docs.ray.io/en/latest/ray-core/fault_tolerance/tasks.html
  - https://docs.ray.io/en/latest/ray-core/fault_tolerance/objects.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task retries

```python
@ray.remote(max_retries=3)                      # default 3; -1 = infinite; 0 = none
def flaky(): ...

@ray.remote(max_retries=5, retry_exceptions=True)          # also retry on Python exceptions
def parse(): ...

@ray.remote(retry_exceptions=[ConnectionError, TimeoutError])   # only these
def fetch(): ...

try:
    ray.get(flaky.remote())
except ray.exceptions.WorkerCrashedError: ...
except ray.exceptions.RayTaskError as e: print(e.cause)        # original exception, if its type can't be subclassed
```

By default Ray retries system failures (worker process died, machine failed), not exceptions raised by your code (`retry_exceptions` is `False`). `RAY_TASK_MAX_RETRIES` overrides the default retry count for all tasks.

## Gotchas
- Retried tasks must be idempotent; side effects (DB inserts, S3 writes) run again.
- If an object value is lost (node died) and no other copy exists, Ray re-executes the producing task (lineage reconstruction), up to `max_retries`, if the object's owner is alive. Lineage over `RAY_max_lineage_bytes` (default 1 GiB) is evicted; objects from `ray.put` and, by default, actor task results cannot be reconstructed.
- With reconstruction disabled (for example `RAY_TASK_MAX_RETRIES=0`) and all copies lost, `ray.get` raises `ObjectLostError`.
- Override per call: `f.options(max_retries=0).remote()`.
- Actor tasks use `max_task_retries` (see actor-restarts).

## Verify
Make a task call `os._exit(0)` with some probability (as the Ray docs example does) and confirm `ray.get` still returns with `max_retries=1`; `ray list tasks -f task_id=<id>` shows the failed attempt and its retry.

## Checked
2026-11-03: checked against the Ray docs source `core/fault-tolerance/tasks.md`, `core/fault-tolerance/objects.md` and `core/doc_code/tasks_fault_tolerance.py`. Removed the unsourced claim that `max_retries=0` plus node loss alone raises `ObjectLostError` and the PID-kill verification.
Method: documentation only; no commands were run.
