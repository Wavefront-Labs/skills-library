---
id: computing-software.database-administration.time-series-databases.mimir-architecture
name: mimir-architecture
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-mimir, mimir-architecture, prometheus, mimir]
level: practitioner
status: draft
description: "Understand Mimir's components to plan a scalable Prometheus long-term store."
sources:
  - https://grafana.com/docs/mimir/latest/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mimir architecture

**Goal:** Understand Mimir's components to plan a scalable Prometheus long-term store.

## Steps
- Write path: distributor (validates, shards by tenant and series hash) to ingesters (in-memory head, WAL, replicate factor 3 by default).
- Read path: query-frontend (splitting, caching) to querier to ingesters plus store-gateway (object-store blocks).
- Background: compactor, ruler for recording/alerting rules, alertmanager, optional query-scheduler.
- Storage: S3-compatible object store holds blocks; ingesters hold about 2 hours locally.
- Deployment modes: monolithic (`-target=all`), read-write, or microservices; start with monolithic or read-write.
- Prometheus pushes with `remote_write` to `/api/v1/push`; set `X-Scope-OrgID` for tenants.

**Gotcha:** Running ingesters with fewer than three zones or replicas risks data loss on node failure; follow replication guidance.

## Verify
- `cortex_distributor_received_samples_total` increases.
- Query via Grafana datasource returns recent and older data.
