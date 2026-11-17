---
id: computing-software.devops-ci-cd.concourse-ci.container-placement-strategies
name: container-placement-strategies
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [container-placement, volume-locality, fewest-build-containers, limit-active-tasks, random, web-node]
level: practitioner
status: docs-checked
description: "Choose how the web node places get, put and task containers across workers: volume-locality, fewest-build-containers, random, limit-active-tasks, with env vars and trade-offs."
sources:
  - https://concourse-ci.org/docs/operation/container-placement/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every step runs in a container, and the web node picks the worker according to `CONCOURSE_CONTAINER_PLACEMENT_STRATEGY`. If no worker satisfies the strategy the step blocks until one does.

- **volume-locality** (the default) places `task` and `put` containers where most of their inputs already are, avoiding streaming large artifacts from one worker through the web node to another. The drawback is builds gravitating to one worker and overloading it until resource caches warm across the pool.
- **fewest-build-containers** places `get`, `put` and `task` containers on the worker with the fewest build containers. Check containers are not counted because they are long-lived and reused. Suited to builds light on artifacts and heavy on task execution.
- **random** puts containers on any worker, ignoring affinity.
- **limit-active-tasks** counts active tasks per worker and places containers on the worker with the fewest. Optionally set `CONCOURSE_MAX_ACTIVE_TASKS_PER_WORKER` to 1 or more; 0 means unlimited. When every worker is at the cap the task waits, polling the pool, and the metric `concourse_steps_waiting{type="task"}` is emitted. The cap does not apply to `get` and `put`.

```properties
CONCOURSE_CONTAINER_PLACEMENT_STRATEGY=limit-active-tasks
CONCOURSE_MAX_ACTIVE_TASKS_PER_WORKER=1
```

The `limit-active-containers` and `limit-active-volumes` strategies are covered separately because they only filter workers and are meant to be chained.

## Checked

2026-11-04. Strategy behaviour, defaults, env vars and the waiting metric confirmed on the Container Placement page.

Method: documentation only; no commands were run.
