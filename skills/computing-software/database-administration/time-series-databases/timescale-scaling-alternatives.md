---
id: computing-software.database-administration.time-series-databases.timescale-scaling-alternatives
name: timescale-scaling-alternatives
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-timescale-multinode, timescale-scaling-alternatives, timescaledb, postgresql]
level: practitioner
status: draft
description: "Choose how to scale Timescale beyond one node."
sources:
  - https://docs.timescale.com/
  - https://www.postgresql.org/docs/current/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scaling alternatives

**Goal:** Choose how to scale Timescale beyond one node.

## Steps
- Vertical: more CPU, RAM and NVMe; compression cuts storage 90 percent for metrics (varies).
- Reads: streaming replicas plus a connection pooler (pgbouncer) and continuous aggregates for dashboards.
- Ingest: batch via `COPY` and `timescaledb-parallel-copy`, tune chunk interval, drop unneeded indexes.
- Storage tiering: Timescale cloud offers tiered object storage (confirm; not in self-hosted community).
- Partition by tenant into multiple databases or clusters when a single node is saturated.
- Compare against purpose-built distributed options (ClickHouse, Mimir) when you need many nodes.

**Gotcha:** More indexes slow inserts proportionally; every extra index on a hot chunk costs write throughput.

## Verify
- Ingest benchmark reaches target rows per second with the final index set.
- Replica lag stays below the dashboard staleness budget.
