---
id: computing-software.ai-ml-engineering.ray.placement-groups
name: placement-groups
category: computing-software
field: ai-ml-engineering
product: ray
tags: [ai-ml-engineering, ray, placement-group, bundles, strict-pack, gang-scheduling]
level: practitioner
status: docs-checked
description: "Reserve co-located or spread resource bundles in Ray with placement groups (PACK, SPREAD, STRICT_*), schedule into bundles, and clean up."
sources:
  - https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html
  - https://docs.ray.io/en/latest/ray-core/api/doc/ray.util.placement_group.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Placement groups

```python
from ray.util.placement_group import placement_group, remove_placement_group
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy

pg = placement_group([{"CPU": 2, "GPU": 1}] * 4, strategy="STRICT_SPREAD")  # one bundle per node
ray.get(pg.ready(), timeout=120)                    # raises a timeout error if the group is not placed in time

@ray.remote(num_cpus=2, num_gpus=1)
class Worker: ...
workers = [Worker.options(scheduling_strategy=PlacementGroupSchedulingStrategy(
              placement_group=pg, placement_group_bundle_index=i)).remote() for i in range(4)]
remove_placement_group(pg)
```
Strategies: `PACK` (best effort), `SPREAD` (best effort), `STRICT_PACK` (one node), `STRICT_SPREAD` (distinct nodes).

## Gotchas
- Reservation is atomic (gang): all bundles or none; check `pg.ready()` and `ray status` for pending placement groups.
- Reserved resources can be used only by tasks and actors scheduled with `PlacementGroupSchedulingStrategy`; several can share one bundle.
- Child tasks and actors do not use the parent's group unless `placement_group_capture_child_tasks=True` (override with `PlacementGroupSchedulingStrategy(placement_group=None)`).
- A group lives as long as the driver (or detached actor) that created it; `lifetime="detached"` keeps it alive past the job, and `remove_placement_group` frees it early.
- Ray Train and Tune use the placement group APIs for gang scheduling.

## Verify
`ray list placement-groups` shows `CREATED`; distinct node IDs across workers for STRICT_SPREAD.

## Checked
2026-11-03: checked against the Ray docs source `core/scheduling/placement-group.md` and `core/doc_code/placement_group_example.py`. Removed the unsourced "forever pending" and ScalingConfig claims.
Method: documentation only; no commands were run.
