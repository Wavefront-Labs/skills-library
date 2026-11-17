---
id: computing-software.database-administration.time-series-databases.victoriametrics-single-vs-cluster
name: victoriametrics-single-vs-cluster
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-victoriametrics, victoriametrics-single-vs-cluster, prometheus, victoriametrics]
level: practitioner
status: draft
description: "Pick and deploy the right VictoriaMetrics topology."
sources:
  - https://docs.victoriametrics.com/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Single node versus cluster

**Goal:** Pick and deploy the right VictoriaMetrics topology.

## Steps
- Single-node (`victoria-metrics-prod -storageDataPath=/vm-data -retentionPeriod=12`) handles millions of samples per second on one host; retentionPeriod unit is months by default, or use suffixes like `30d`.
- Cluster version splits vminsert (ingest), vmstorage (data) and vmselect (query); scale each separately.
- Storage replication via `-replicationFactor=2` on vminsert (cluster).
- Prometheus remote write: `http://vm:8428/api/v1/write` (single) or `.../insert/0/prometheus/api/v1/write` (cluster tenant 0).
- Query endpoint is Prometheus-compatible (`/api/v1/query`); MetricsQL extends PromQL.
- Start single-node; move to cluster when one host can no longer hold the data or throughput.

**Gotcha:** Data in single-node mode cannot be spread over several machines; plan the cluster path before you outgrow disk.

## Verify
- `/metrics` shows ingestion rates and merge status.
- Grafana with a Prometheus datasource pointed at VM returns data.
