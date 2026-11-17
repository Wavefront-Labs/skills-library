---
id: computing-software.ai-ml-engineering.ray.actors
name: actors
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-actor, actor-class, actor-handle, stateful-worker]
level: practitioner
status: docs-checked
description: "Create stateful Ray actors with @ray.remote classes, call methods via handles, pass handles to tasks, and know the concurrency model."
sources:
  - https://docs.ray.io/en/latest/ray-core/actors.html
  - https://docs.ray.io/en/latest/ray-core/actors/concurrency_group_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Actors

```python
@ray.remote
class Counter:
    def __init__(self, start=0): self.n = start
    def incr(self, k=1): self.n += k; return self.n
    def get(self): return self.n

c = Counter.remote(10)                               # starts a dedicated worker process
refs = [c.incr.remote() for _ in range(5)]           # executed serially, in call order (same submitter)
print(ray.get(refs), ray.get(c.get.remote()))        # [11..15] 15

@ray.remote
def use(counter): return ray.get(counter.incr.remote())   # handles can be passed into tasks
ray.get(use.remote(c))
ray.kill(c)                                          # force terminate
```
Actor resources: `@ray.remote(num_cpus=2, num_gpus=1)`.

## Gotchas
- Methods on the same actor run serially; methods on different actors run in parallel. For concurrency inside one actor use `max_concurrency` or an async actor.
- State lives in one process; if it dies the state is lost unless you set `max_restarts` and rebuild in `__init__`.
- Actor state is per instance and per process; class variables are not shared between actors. Share state through another actor and pass its handle.
- Ray terminates a non-detached actor when all its handles go out of scope or its creator dies; keep a reference.

## Verify
`ray list actors` (state CLI) shows the actor `ALIVE`; sequential increments return consecutive values.

## Checked
2026-11-03: checked against the Ray docs source `core/actors/index.md`, `core/actors/terminating-actors.md` and `core/fault-tolerance/actors.md`. Removed the unsourced handle-attribute and constructor-exception claims.
Method: documentation only; no commands were run.
