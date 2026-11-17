---
id: computing-software.cloud-infrastructure-engineering.cortex.cortex-monitoring-assets
name: cortex-monitoring-assets
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [monitoring, dashboards, alerts, recording-rules, mixin]
level: practitioner
status: docs-checked
description: "Install the Grafana dashboards, alert rules and recording rules bundled with Cortex and know which dashboard to open first."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/monitoring-cortex.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex ships production monitoring assets in the repository, generated from a jsonnet mixin that is the source of truth:

- Dashboards (JSON) in `docs/getting-started/dashboards/`, importable via Grafana Dashboards, Import, Upload JSON file.
- Alert rules in `docs/getting-started/alerts.yaml`: more than 50 PrometheusRule alerts grouped by component.
- Recording rules in the cortex-mixin `recording_rules.libsonnet`, pre-aggregated series used by dashboards and alerts.

Key dashboards:

- `cortex-writes.json`: write path end to end (distributor QPS, ingestion rate, ingester push errors and latency, samples appended, WAL writes). Open first during a write incident.
- `cortex-reads.json`: query QPS at the frontend, scheduler queue length, querier latency, store-gateway and ingester sub-queries.
- `cortex-queries.json`: per-query chunks and series fetched, bytes processed, queries by tenant; for hunting expensive queries.
- `cortex-slow-queries.json`: slowest recent queries with PromQL and tenant; pair with query-frontend logs.
- `cortex-compactor.json`: compaction progress.

Install the recording rules too, since dashboards and alerts depend on them.

## Checked

Method: docs-checked 2026-11-09 against the full Cortex monitoring-cortex.md (raw markdown, master). Asset paths, dashboard purposes and the recording-rule dependency all match the page.
