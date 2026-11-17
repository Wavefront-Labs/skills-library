---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-tempo
name: monitoring-tempo
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [tempo-metrics, tempo-dashboards, tempo-mixin, tempo, self-monitoring]
level: practitioner
status: docs-checked
description: "Monitor Grafana Tempo itself: build and load the tempo-mixin dashboards, rules and alerts, and know what each dashboard covers."
sources: ["https://grafana.com/docs/tempo/latest/operations/monitor/", "https://github.com/grafana/tempo/tree/main/operations/tempo-mixin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Tempo

Tempo exposes Prometheus metrics (RED metrics for most services and backends), logfmt logs and self-traces. The Tempo
repository ships a mixin with dashboards, rules and alerts for production monitoring.

## Get the mixin
Use the prebuilt files in `operations/tempo-mixin-compiled` (dashboards as JSON, `alerts.yaml`, `rules.yaml`), or build
your own after changing the jsonnet. Building needs jsonnet and jsonnet-bundler (`jb`):
```bash
cd operations/tempo-mixin
make all    # runs jb install, then writes dashboards, alerts.yaml and rules.yaml to ../tempo-mixin-compiled
```
Load the YAML rules and alerts into your Prometheus, and import the dashboard JSON into Grafana. The dashboards suit
Kubernetes deployments whose scraped metrics carry `cluster` and `namespace` labels.

## Dashboards (from the docs)
- Reads and Writes: RED for the query path (gateway, query-frontend, queriers, live-stores) and the ingest path
  (gateway, distributors, Kafka); use them to size replicas.
- Resources: CPU, container memory and Go heap in use per component.
- Backend Work: blocklist length and poll duration, compaction jobs, backend-scheduler and backend-worker resources.
- Block Builder: Kafka-based ingest throughput and partition lag.
- Rollout Progress: request status codes, p99 latency, unhealthy pods and version counts during upgrades.
- Tenants: per-tenant ingestion, reads, storage and metrics-generator series.
- Service Graph, Livestore, and Operational (a large catalogue of metrics worth considering, not a model dashboard).

## Metric worth knowing
`tempo_query_frontend_bytes_inspected_total` counts bytes inspected by the query path behind the query frontend, per
tenant and op (traces, search, metadata, metrics); cached querier responses are excluded.

## Alerts
Rules and alerts are YAML in the compiled mixin; the mixin `runbook.md` explains how to fix firing alerts.

## Verify
- [ ] Imported dashboards show data for your `cluster` and `namespace` labels.

## Checked

2026-11-08. Confirmed against the Tempo Monitor page and the tempo-mixin README. Removed as unconfirmed: the metric
table (other metric names), the alert name list, the discard-reason tuning advice, the Helm serviceMonitor values and
the verification query. The troubleshooting source was not read and was dropped.
Method: documentation only; no commands were run.
