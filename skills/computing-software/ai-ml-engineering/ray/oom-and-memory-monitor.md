---
id: computing-software.ai-ml-engineering.ray.oom-and-memory-monitor
name: oom-and-memory-monitor
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, memory-monitor, oomkilled, out-of-memory, memory-usage-threshold]
level: practitioner
status: docs-checked
description: "Handle Ray out-of-memory: the raylet memory monitor, its retry and worker-killing policy, OutOfMemoryError, threshold env vars and fixes."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/ray-oom-prevention.html
  - https://docs.ray.io/en/latest/ray-core/scheduling/memory-management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OOM and the memory monitor

Each raylet runs a memory monitor (Linux; tested in containers with cgroup v1 or v2). It counts worker heap, object store and raylet memory, and kills a task or actor process when usage crosses a threshold. It is on by default.

```bash
RAY_memory_usage_threshold=0.9 ray start --head          # default 0.95; fraction of node memory
RAY_memory_monitor_refresh_ms=250 ray start ...           # check interval, default 250; 0 disables killing (only if resource isolation is off)
```
Errors:
```python
try:
    ray.get(ref)
except ray.exceptions.OutOfMemoryError as e:
    print(e)          # the task failed because the memory monitor killed it
```
Mitigation patterns:
```python
@ray.remote(memory=8 * 1024**3)                         # bytes; admission control only, does not limit usage
def heavy(chunk): ...
@ray.remote(num_cpus=4)                                  # reduce task parallelism by requesting more CPUs per task
```
Process data in smaller blocks and use `ray memory` to find objects pinned by references.

## Gotchas
- A killed task or actor is retried with exponential backoff (delay capped at 60 s). Killed tasks are retried indefinitely and ignore `max_retries`, unless `max_retries=0`, in which case they are not retried. Actors respect `max_restarts` (default 0).
- The monitor ensures at least one task per caller can run on each node; if it cannot, the workload fails with an OOM error even when `max_retries=-1`.
- Since Ray 2.56 the policy kills idle workers first (largest memory footprint first), then active workers, preferring retryable tasks and then the newest lease. `RAY_worker_killing_policy_by_group=true` (set before starting Ray) restores the legacy policy, which picks from the caller with the most running tasks and kills its latest-started task.
- Actors are not retryable by default (`max_restarts` is 0), so by default tasks are killed before actors.
- Object store memory counts toward the usage the monitor tracks.

## Verify
A task that exceeds the threshold fails with `OutOfMemoryError` (with `max_retries=0`); after reducing parallelism or data size it no longer does.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/ray-oom-prevention.md`, `core/scheduling/memory-management.md` and `core/doc_code/ray_oom_prevention.py`. Fixed: killed tasks are retried indefinitely and ignore `max_retries` (only `max_retries=0` stops it); added the real killing policy. Removed the unsourced `OOMKilled`, log-grep and `max_retries=2` claims.
Method: documentation only; no commands were run.
