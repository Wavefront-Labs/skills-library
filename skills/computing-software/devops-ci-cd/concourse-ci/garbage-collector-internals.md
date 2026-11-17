---
id: computing-software.devops-ci-cd.concourse-ci.garbage-collector-internals
name: garbage-collector-internals
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [garbage-collection, gc, containers, volumes, grace-period, database, workers]
level: advanced
status: docs-checked
description: "Learn how Concourse garbage collection works: the 30-second batch, database rows first then asynchronous per-object collectors, and the safe, airtight, resilient goals."
sources:
  - https://concourse-ci.org/docs/internals/garbage-collector/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every step runs in fresh containers and volumes, so Concourse needs a safe way to remove them afterwards. The documented goals:

- **Safe**: never remove a container or volume from under a running build, and never break check containers.
- **Airtight**: nothing leaks. Every container, volume or database row has a defined lifecycle, and the ATC can be interrupted at any point and still clean up what it created.
- **Resilient**: collection is not outpaced by the workload, one misbehaving worker does not block others, and one slow delete does not block other objects on the same worker.

**Mechanism.** The collector is a batch operation on an interval, default 30 seconds. It must finish quickly enough not to be outpaced. First it collects within the database alone, removing rows no longer needed; removals at one stage often cause removals later. Each object type has its own collector (volume collector, container collector and so on) and all run asynchronously.

That pass leaves a set of containers and volumes eligible for removal. These are harder because they need a worker to delete them, possibly slowly. They are the costliest resources Concourse consumes, so deleting is parallelised so one slow worker or delete does not let them pile up.

On the worker side this meets the TSA commands `sweep-containers`, `sweep-volumes`, `report-containers` and `report-volumes`; see the worker lifecycle skill. Grace periods are tuned in the performance tuning skill.

## Checked

2026-11-04. Goals, interval and two-phase process confirmed on the Garbage Collector page; sweep and report commands on the Internals page.

Method: documentation only; no commands were run.
