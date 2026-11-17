---
id: computing-software.ai-ml-engineering.ray.actor-restarts
name: actor-restarts
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, max-restarts, max-task-retries, actor-fault-tolerance, ray-actor-error]
level: practitioner
status: docs-checked
description: "Make Ray actors survive crashes with max_restarts and max_task_retries, handle RayActorError, and restore state on restart."
sources:
  - https://docs.ray.io/en/latest/ray-core/fault_tolerance/actors.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.remote.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Actor fault tolerance

```python
@ray.remote(max_restarts=4, max_task_retries=2)    # restarts: -1 = infinite; default 0
class Worker:
    def __init__(self):
        self.state = load_checkpoint() or {}       # rebuild state from storage here
    def work(self, x): ...
    def __ray_shutdown__(self): ...                # cleanup hook on graceful termination only

w = Worker.remote()
try:
    ray.get(w.work.remote(1))
except ray.exceptions.RayActorError:
    # actor died and the call was not retried, or restarts/retries are exhausted
    ...
```
- `max_restarts`: how many times Ray recreates the actor process after a crash or node loss (calls `__init__` again).
- `max_task_retries`: how many times a method call is retried when the actor is unreachable (default 0 = at-most-once; -1 = unlimited). A nonzero value gives at-least-once execution, so use it only for idempotent methods.
- `ray.kill(a, no_restart=False)` triggers a restart; the default `no_restart=True` does not.

## Gotchas
- In-memory state is lost on restart; persist checkpoints externally.
- A call submitted while the actor is restarting counts as one retry; with the default `max_task_retries=0` such calls can raise `RayActorError`, even if the task actually ran.
- To retry a method on application exceptions, set `max_task_retries` with `retry_exceptions` (`@ray.method(retry_exceptions=...)`).
- Ray does not restart an actor whose creator died, but it keeps restarting a `lifetime="detached"` actor until `max_restarts` is exhausted.
- If checkpoints live in external storage, make them reachable from every node: Ray can restart the actor on a different one.

## Verify
Crash the actor process (for example `os._exit(1)` inside a method) and call it again: with `max_restarts` and `max_task_retries` set the call succeeds after the restart; `ray list actors --detail` shows the death cause of a dead actor.

## Checked
2026-11-03: checked against the Ray docs source `core/fault-tolerance/actors.md`, `core/actors/terminating-actors.md` and the `ray.kill` docstring in `python/ray/_private/worker.py`. Fixed the shutdown hook name (`__ray_shutdown__`, not `__ray_terminate__`). Removed the unsourced `num_restarts` and exception-no-restart claims.
Method: documentation only; no commands were run.
