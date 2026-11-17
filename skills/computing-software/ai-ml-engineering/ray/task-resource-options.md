---
id: computing-software.ai-ml-engineering.ray.task-resource-options
name: task-resource-options
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, num-gpus, num-cpus, ray-resources, memory-option]
level: practitioner
status: docs-checked
description: "Request CPU, GPU, memory and custom resources for Ray tasks with @ray.remote and .options(), fractional GPUs, and what the numbers mean."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/resources.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.remote.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task resource options

```python
@ray.remote(num_cpus=2, num_gpus=0.5, memory=4 * 1024**3)
def train_shard(x): ...

train_shard.options(num_cpus=4).remote(x)          # per-call override
@ray.remote(num_gpus=1)
def gpu_job():
    import os; return os.environ["CUDA_VISIBLE_DEVICES"]   # Ray sets this
```
Defaults: a task uses one logical CPU; an actor uses one logical CPU for scheduling and zero for running, so always set `num_cpus` explicitly for actors. Resources you specify explicitly are required both at schedule time and at execution time. Fractional values work (precision 0.0001); GPU requirements above 1 must be whole numbers.

## Gotchas
- Resources are logical and used for admission control: Ray does not stop a `num_cpus=1` task from using several threads or CPUs. Setting `num_cpus` makes Ray set `OMP_NUM_THREADS=<num_cpus>` (1 if unset); set it yourself to override.
- Ray gives GPU isolation only as visible devices (`CUDA_VISIBLE_DEVICES`). `num_gpus=0.5` lets tasks share a GPU; make sure each stays within its share of the accelerator memory.
- `memory` is in bytes and is only used for admission control during scheduling; it does not limit usage.
- Resource requirements are hard: if no node has the requested resources (a GPU task on a CPU-only cluster), Ray cannot schedule the task until a feasible node is added.

## Verify
The function returns the expected `CUDA_VISIBLE_DEVICES`.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/resources.md`, `core/scheduling/accelerators.md`, `core/scheduling/memory-management.md`, `core/scheduling/index.md`. Fixed the default task CPU claim and the OMP_NUM_THREADS note; removed the unsourced hang/autoscaler, torch-import and `ray status` claims.
Method: documentation only; no commands were run.
