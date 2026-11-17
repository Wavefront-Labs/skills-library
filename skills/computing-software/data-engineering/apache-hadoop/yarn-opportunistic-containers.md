---
id: computing-software.data-engineering.apache-hadoop.yarn-opportunistic-containers
name: yarn-opportunistic-containers
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, opportunistic-containers, distributed-scheduling, queuing]
level: advanced
status: docs-checked
description: "YARN opportunistic containers: the three enabling properties and defaults, central versus distributed allocation, NM queuing and kill order, and MapReduce percentage."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/OpportunisticContainers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Opportunistic containers

Execution type is set per container by the AM; the default is GUARANTEED. An OPPORTUNISTIC container can be dispatched to an NM even if it cannot start immediately; it queues there until resources free up. The aim is better utilisation and throughput, most noticeably for short tasks (seconds). Opportunistic containers are lower priority and can be preempted (killed) for guaranteed ones.

Enable in conf/yarn-site.xml:
- `yarn.resourcemanager.opportunistic-container-allocation.enabled` = true (default false)
- `yarn.nodemanager.opportunistic-containers-max-queue-length`: default 0; must be positive to allow queuing. 10 is suggested to start experimenting; the best value depends on workload, cluster and target utilisation.
- Optional `yarn.nodemanager.distributed-scheduling.enabled` (default false) for distributed allocation; guaranteed containers still go through the RM. A client submitting to a cluster with AMRMProxy on needs its own config with `yarn.resourcemanager.scheduler.address` = `localhost:8049`.

Advanced defaults (usually fine): `yarn.resourcemanager.opportunistic-container-allocation.nodes-used` 10; `yarn.resourcemanager.nm-container-queuing.sorting-nodes-interval-ms` 1000, `queue-limit-stdev` 1.0f (the k in avg + k*stdev), `min-queue-length` 5, `max-queue-length` 15; `yarn.nodemanager.amrmproxy.address` 0.0.0.0:8049, `yarn.nodemanager.amrmproxy.client.thread-count` 3.

Allocation:
- Central (default): the RM's `OpportunisticContainerAllocatorAMService` splits requests; guaranteed ones go to the existing scheduler, opportunistic ones to the `OpportunisticContainerAllocator`, which assigns to the least loaded nodes round-robin. It deliberately ignores locality and does not apply fairness/capacity constraints.
- Distributed: the NM's `AMRMProxyService` intercepts AM traffic; its `DistributedScheduler` places opportunistic containers without contacting the RM, using a least-loaded-nodes list the RM sends via heartbeats. Only guaranteed requests are forwarded.
- Load is judged only by queued opportunistic container counts.

Execution at the NM: after localization a container is SCHEDULED. If resources are free it starts whatever its type. If not, a guaranteed container starts after the NM kills enough running opportunistic ones (the page says reverse order of arrival, most recently started first); an opportunistic one stays queued. Queued containers are picked FIFO as resources free.

Load shedding: when queue length exceeds the RM-computed limit, the NM discards opportunistic containers and the AM reschedules them elsewhere.

Jobs: MapReduce `-Dmapreduce.job.num-opportunistic-maps-percent="40"` runs that share of mappers opportunistically. Distributed shell `-container_type OPPORTUNISTIC` (or GUARANTEED); `-promote_opportunistic_after_start` attempts promotion once started; `-enforce_execution_type` makes the scheduler honour the type.

The RM web UI Nodes page gains Running Containers (O), Mem Used (O), VCores Used (O) and Queued Containers columns.

## Checked

Method: 2026-11-08, read the project's OpportunisticContainers markdown source in full against this skill. Replaced the unsupported "Verify" step with the UI columns the page does state, fixed the "three enabling properties" framing (the page says two required plus one for distributed) and added the client AMRMProxy setting and distributed-shell flags. Defaults and kill order were unchanged.
