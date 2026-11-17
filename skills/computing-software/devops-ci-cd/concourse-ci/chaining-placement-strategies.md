---
id: computing-software.devops-ci-cd.concourse-ci.chaining-placement-strategies
name: chaining-placement-strategies
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [container-placement, limit-active-containers, limit-active-volumes, chaining, worker-capacity]
level: advanced
status: docs-checked
description: "Chain Concourse placement strategies: limit-active-containers and limit-active-volumes filters first, then volume-locality and fewest-build-containers, with the example."
sources:
  - https://concourse-ci.org/docs/operation/container-placement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Placement strategies can be comma-chained. The first strategy receives all workers, filters them, and passes the survivors on; if the last strategy still returns several workers, one is chosen at random (an implicit `random` at the end).

The two limit strategies only reject workers and make no effort to find the emptiest one, so they are most useful at the front of a chain:

- `limit-active-containers` rejects workers with too many containers; configure `CONCOURSE_MAX_ACTIVE_CONTAINERS_PER_WORKER` (1 or more).
- `limit-active-volumes` rejects workers with too many volumes; configure `CONCOURSE_MAX_ACTIVE_VOLUMES_PER_WORKER`.

If the max is unset or 0 the strategy has no effect, so as the only strategy workers are chosen at random.

The documented example:

```properties
CONCOURSE_CONTAINER_PLACEMENT_STRATEGY=limit-active-containers,limit-active-volumes,volume-locality,fewest-build-containers
CONCOURSE_MAX_ACTIVE_CONTAINERS_PER_WORKER=200
CONCOURSE_MAX_ACTIVE_VOLUMES_PER_WORKER=100
```

Reading it in order: remove workers over 200 containers; remove remaining workers over 100 volumes; keep only the worker(s) with the most inputs locally (a tie can keep several); break ties by choosing fewer build containers; if still tied, pick at random.

## Checked

2026-11-04. Chain semantics and the four-strategy example confirmed on the Container Placement page, Chaining Placement Strategies section.

Method: documentation only; no commands were run.
