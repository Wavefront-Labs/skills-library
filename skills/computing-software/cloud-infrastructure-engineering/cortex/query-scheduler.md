---
id: computing-software.cloud-infrastructure-engineering.cortex.query-scheduler
name: query-scheduler
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [query-scheduler, query-frontend, queue, scaling]
level: advanced
status: docs-checked
description: "Move the query queue into a separate query scheduler so frontends and queues scale independently."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/scalable-query-frontend.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The query scheduler is an optional stateless service that takes the internal queue out of the query frontend. This lets you scale the number of frontends and the number of queues independently, and run multiple frontends without increasing the number of queues.

To use it, configure both the query frontend and the queriers with the scheduler address: `-frontend.scheduler-address` on the frontend and `-querier.scheduler-address` on queriers. A querier fetches from either a frontend or a scheduler, never both: `-querier.frontend-address` and `-querier.scheduler-address` are mutually exclusive.

The query flow changes: the frontend receives the query (optionally splitting or serving from cache), forwards it to a random query scheduler process, the scheduler stores it in its in-memory queue, a querier picks it up, executes it and sends the result back to the frontend, which returns it to the client.

Run two scheduler replicas: a single one risks higher query latency when it crashes or restarts, and two are enough even for large clusters with high QPS. In single-binary mode Cortex defaults to running without a query scheduler.

Scaling frontends or schedulers changes how many workers each querier runs (each worker connects to one frontend). To keep a querier from taking more queries than it can handle, set `-querier.worker-match-max-concurrent=true` (YAML: `match_max_concurrent: true` under `frontend_worker`) so its PromQL concurrency (`-querier.max-concurrent`) matches its connections.

Configure `/ready` as the load balancer health check: it returns 200 only when the frontend can serve queries, and with a scheduler only after the frontend has discovered schedulers via DNS resolution. Otherwise a frontend scale-up can cause failed queries or high latency while queriers attach.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page and the scaling-the-query-frontend page (raw markdown, both read in full).
