---
id: computing-software.data-engineering.apache-hadoop.yarn-fair-scheduler-allocation-file
name: yarn-fair-scheduler-allocation-file
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, fair-scheduler, allocation-file, queues, drf]
level: practitioner
status: docs-checked
description: "YARN Fair Scheduler: yarn-site properties and defaults, allocation file queue elements, scheduling policies fair/drf/fifo, placement rules and preemption timeouts."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/FairScheduler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fair Scheduler

Select it with `yarn.resourcemanager.scheduler.class`. Key yarn-site.xml properties:
- `yarn.scheduler.fair.allocation.file` (default `fair-scheduler.xml`, resolved on the classpath)
- `yarn.scheduler.fair.user-as-default-queue` (true; ignored if a placement policy is defined)
- `yarn.scheduler.fair.preemption` (false) and `...preemption.cluster-utilization-threshold` (0.8)
- `yarn.scheduler.fair.sizebasedweight` (false), `assignmultiple` (false), `dynamic.max.assign` (true), `max.assign` (-1), `update-interval-ms` (500)

Allocation file elements:
- `queue` (`type="parent"` for a parent without leaves), `minResources`, `maxResources` (enforced up the tree), `maxRunningApps`, `weight` (default 1)
- `schedulingPolicy`: `fifo`, `fair` (default), `drf`, or a custom class; `defaultQueueSchedulingPolicy` at top level
- `userMaxAppsDefault` and per-`user` `maxRunningApps`
- `queuePlacementPolicy`: ordered rules `specified`, `user`, `primaryGroup`, `secondaryGroupExistingQueue`, `nestedUserQueue`, `default`, `reject`; each takes `create` (default true)

Preemption timeouts (seconds, default Long.MAX_VALUE meaning off): `minSharePreemptionTimeout`, `fairSharePreemptionTimeout`; `fairSharePreemptionThreshold` defaults 0.5; `allowPreemptionFrom` defaults true. Root-level `default...` variants are overridden per queue.

The file is reloaded about every 10 seconds; changes apply 10-15 seconds after the scheduler sees the modification.

Verify: after saving, the new queues appear on the RM scheduler page.

## Checked
Confirmed 2026-11-08 against the Apache Hadoop Fair Scheduler page: the yarn-site properties and defaults, queue elements, scheduling policies, the queuePlacementPolicy rule list with the `create` default of true, preemption timeouts and thresholds, and the reload interval. Dropped the claim that no rmadmin command is needed, which the page does not state.
Method: docs-only read of cited pages, 2026-11-08
