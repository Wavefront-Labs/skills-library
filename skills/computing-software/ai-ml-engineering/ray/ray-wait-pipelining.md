---
id: computing-software.ai-ml-engineering.ray.ray-wait-pipelining
name: ray-wait-pipelining
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, ray-wait, as-completed, task-pipelining, backpressure]
level: practitioner
status: docs-checked
description: "Use ray.wait to process Ray task results as they finish, limit in-flight tasks with backpressure and add timeouts."
sources:
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.wait.html
  - https://docs.ray.io/en/latest/ray-core/patterns/limit-pending-tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ray.wait pipelining

```python
MAX_INFLIGHT = 32
pending, results = [], []
for item in items:
    if len(pending) >= MAX_INFLIGHT:                     # backpressure
        done, pending = ray.wait(pending, num_returns=1)
        results.extend(ray.get(done))
    pending.append(process.remote(item))
while pending:
    done, pending = ray.wait(pending, num_returns=len(pending), timeout=60)
    if not done: raise TimeoutError("stuck")
    results.extend(ray.get(done))

ready, not_ready = ray.wait(refs, num_returns=1, timeout=5, fetch_local=False)
```

## Gotchas
- `ray.get(list)` waits for all; `ray.wait` returns completed ones first, enabling streaming and early exit.
- Submitting tasks faster than they finish grows the pending-task queue and can cause OOM, mainly for an endless stream of tasks; cap in-flight refs as above.
- `timeout` is in seconds; when `None`, Ray uses 10**6 seconds.
- The refs passed to `ray.wait` must be unique.
- `fetch_local=False` avoids pulling results to the caller's node when you only need to know completion.

## Verify
Memory usage of the driver stays flat when you scale `items` up.

## Checked
2026-11-03: checked against the `ray.wait` docstring in `python/ray/_private/worker.py` and the Ray docs patterns page `limit-pending-tasks`. Removed the unsourced 1M-task claim, the `timeout=0` and failed-task-as-ready claims and the `ray status` check.
Method: documentation only; no commands were run.
