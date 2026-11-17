---
id: computing-software.ai-ml-engineering.ray.custom-resources
name: custom-resources
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, custom-resources, resources-flag, accelerator-type, ray-start-resources]
level: practitioner
status: docs-checked
description: "Define and consume custom Ray resources (ray start --resources, resources={...}) and accelerator_type to target specific hardware."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/resources.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.remote.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom resources

Declare when starting a node; request in tasks.

```bash
ray start --head --resources='{"ssd": 2, "licence": 1}' --num-gpus=4
ray start --address=HEAD:6379 --resources='{"ssd": 4}'
```
```python
ray.init(resources={"ssd": 2})                      # single-node cluster started by ray.init

@ray.remote(resources={"ssd": 1})                   # logical units, a float quantity
def read_local(): ...

@ray.remote(num_gpus=1, accelerator_type=NVIDIA_TESLA_V100)   # from ray.util.accelerators import NVIDIA_TESLA_V100
def gpu_job(): ...
```
In KubeRay, set `rayStartParams: { resources: '"{\"ssd\": 2}"' }` (note the quoting) in the worker group.

## Gotchas
- Custom resource names are arbitrary strings; a request no node can satisfy is infeasible and the task is not scheduled until a feasible node joins. Compare with `ray.cluster_resources()`.
- Fractional values are allowed (precision 0.0001).
- You cannot update a node's resource capacities after Ray starts on it.
- For label-style targeting Ray calls custom resources a legacy pattern; use them mainly for numeric quantities.
- Use a limited resource such as `{"licence": 1}` to serialise access to a licensed or exclusive device.
- `accelerator_type` is implemented as the custom resource requirement `"accelerator_type:<type>": 0.001`, which also tells the autoscaler there is demand for that type.

## Verify
`ray.cluster_resources()` shows `ssd: 6.0`; at most 6 `ssd: 1` tasks run at once.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/resources.md`, `core/scheduling/accelerators.md` and `core/scheduling/index.md`. Replaced the unsourced `"A100"` accelerator string with the documented `NVIDIA_TESLA_V100` constant; removed the unsourced auto-detection claim and the "confirm" marker.
Method: documentation only; no commands were run.
