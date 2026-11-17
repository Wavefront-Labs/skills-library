---
id: computing-software.cloud-infrastructure-engineering.cortex.query-frontend-queueing-splitting-caching
name: query-frontend-queueing-splitting-caching
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [query-frontend, queueing, splitting, caching, fair-scheduling]
level: practitioner
status: docs-checked
description: "Use the optional query frontend for fair per-tenant queueing, day-splitting and result caching in front of queriers."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The query frontend is optional but accelerates reads. Send queries to it instead of the queriers; queriers still execute the work, pulling jobs from the frontend's queue. Queriers need `-querier.frontend-address` to connect. It is stateless, but run a few replicas (two usually suffice) to benefit from fair scheduling.

Flow: the frontend receives the query, optionally splits it or serves it from cache; queues it; a querier picks it up, executes it and returns the result; the frontend forwards it to the client.

Queueing does three things: retries large queries that OOM a querier (so you can under-provision memory), uses FIFO to avoid convoying large requests on one querier, and schedules fairly between tenants so one cannot DoS the others.

Splitting breaks multi-day queries into single-day queries executed in parallel and stitched together, avoiding OOMs and speeding them up.

Caching stores query results and reuses them; if cached results are incomplete the frontend computes only the missing subqueries. Queries can optionally be aligned to their step to improve cacheability. Supported cache backends are memcached, redis and an in-memory cache.

The frontend can also accelerate any Prometheus-API compatible service, such as Thanos Querier or a Prometheus server, by setting `-frontend.downstream-url`.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full).
