---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.bulkhead
name: bulkhead
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, bulkhead, resource-isolation, connection-pools, thread-pools, semaphore-isolation, noisy-neighbour, tenant-isolation, fault-isolation]
level: practitioner
status: docs-checked
description: "Partition resources so one failing dependency or consumer can't exhaust the rest: per-service pools and semaphores, partitioned service instances and wider isolation."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/bulkhead", "https://resilience4j.readme.io/docs/bulkhead"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bulkhead

Isolate elements of an application into pools so that if one fails the others keep working, and a fault does not
cascade (Azure Architecture Center).

## Levels
1. **Consumer side**: a consumer that calls several services gets a separate connection pool (or thread pool) per
   service. If one service fails, only the pool assigned to it is affected. Resilience4j offers a semaphore-based
   `Bulkhead` (`maxConcurrentCalls`, `maxWaitDuration` for how long a thread may block entering a saturated bulkhead)
   and a thread-pool bulkhead with a bounded queue and fixed pool.
2. **Service side**: partition service instances into groups by consumer load and availability requirements, so one
   consumer that overwhelms its instance does not affect the others; a high-priority consumer pool can use
   high-priority services.
3. **Wider**: separate deployments, queues or consumer pools per workload follow the same idea.

## Sizing
Define partitions around the business and technical requirements. With Resilience4j's semaphore bulkhead it is up to
you to size the thread pools consistently with the bulkhead configuration. Little's law (concurrency = rate x
latency) is a starting estimate; leave headroom and keep each bulkhead well below the total pool.

## Gotchas
- A shared client with one global connection pool undoes in-process bulkheads.
- Rejected calls need a clear fast error and a metric, otherwise it looks like random failure.

## Verify
- [ ] Make one dependency hang: p99 for endpoints not using it is unchanged.
- [ ] A rejection metric exists per bulkhead.

## Checked
2026-11-01. Confirmed in the Azure Architecture Center Bulkhead pattern (pools per service, partitioned instances,
priority pools, partitioning guidance) and the Resilience4j Bulkhead page (semaphore and thread-pool variants,
`maxConcurrentCalls`, `maxWaitDuration`, client-side pool sizing). Little's law is arithmetic. Removed: Polly
`ConcurrencyLimiter`, the 200 req/s worked numbers and headroom factor, tenant deployment-stamp claim, database
`max_connections`/proxy advice, the `maxWaitDuration=0` default wording.
Method: documentation only; no commands were run.
