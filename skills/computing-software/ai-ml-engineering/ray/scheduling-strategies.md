---
id: computing-software.ai-ml-engineering.ray.scheduling-strategies
name: scheduling-strategies
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, node-affinity, spread-strategy, scheduling-strategy, label-selector]
level: practitioner
status: docs-checked
description: "Control Ray task and actor placement with scheduling_strategy: DEFAULT, SPREAD, NodeAffinitySchedulingStrategy and placement group strategies."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/index.html
  - https://docs.ray.io/en/latest/ray-core/scheduling/ray-oom-prevention.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduling strategies

```python
from ray.util.scheduling_strategies import NodeAffinitySchedulingStrategy

@ray.remote(scheduling_strategy="SPREAD")            # spread across nodes
def work(): ...

node_id = ray.get_runtime_context().get_node_id()
pin = NodeAffinitySchedulingStrategy(node_id=node_id, soft=False)   # hard pin (fails if node gone)
work.options(scheduling_strategy=pin).remote()
soft = NodeAffinitySchedulingStrategy(node_id=node_id, soft=True)   # prefer, else anywhere

@ray.remote(scheduling_strategy="DEFAULT")           # favors nodes already holding tasks, then low utilization; random among the top k
```
Pick node IDs with `ray.nodes()` (field `NodeID`; `Alive` says whether the node is up). A strategy that is not `DEFAULT` ignores data locality.

## Gotchas
- `DEFAULT` prefers nodes that already have tasks or actors scheduled, then nodes with low utilization (`RAY_scheduler_spread_threshold` 0.5, `RAY_scheduler_top_k_fraction` 0.2); `SPREAD` tries to spread across available nodes.
- With `soft=False`, a node that is gone or lacks the resources makes the task fail with `TaskUnschedulableError` (`ActorUnschedulableError` for actors); `soft=True` falls back to another feasible node.
- Use `NodeAffinitySchedulingStrategy` only when higher-level options such as placement groups cannot do the job: it cannot fully use an autoscaling cluster because you must know node IDs up front.
- To target hardware kinds, use custom resources (see custom-resources) or labels (a beta feature).
- Head node typically has CPUs too; set `--num-cpus=0` on the head to keep user tasks off it.

## Verify
Return `ray.get_runtime_context().get_node_id()` from 20 tasks and count the distinct node IDs.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/index.md`, `core/scheduling/resources.md` and `core/miscellaneous.md`. Removed the unsourced child-inheritance claim and the "confirm" markers.
Method: documentation only; no commands were run.
