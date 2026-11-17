---
id: computing-software.database-administration.time-series-databases.mimir-ingesters-compactor
name: mimir-ingesters-compactor
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-mimir, mimir-ingesters-compactor, prometheus, mimir]
level: practitioner
status: draft
description: "Operate Mimir ingesters and compactors with proper limits."
sources:
  - https://grafana.com/docs/mimir/latest/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ingesters, limits and compactor

**Goal:** Operate Mimir ingesters and compactors with proper limits.

## Steps
- Ingester memory is driven by active series; set per-tenant limits such as `max_global_series_per_user` and `ingestion_rate`.
- Ingesters need persistent volumes for WAL and use a ring in memberlist or consul/etcd.
- Scale ingesters gradually; zone-aware replication with `-ingester.ring.zone-awareness-enabled`.
- Compactor merges blocks per tenant, sharded by `-compactor.compaction-jobs-order` / split-and-merge settings; scale out by adding replicas.
- Retention per tenant: `compactor_blocks_retention_period` (limits).
- Watch `cortex_ingester_memory_series`, `cortex_ingester_tsdb_*`, `cortex_compactor_runs_failed_total`.

**Gotcha:** Hitting a tenant's series limit makes writes fail with 4xx for new series while existing ones still ingest.

## Verify
- Per-tenant series and rate stay below limits.
- Compactor completes cycles without failures.
