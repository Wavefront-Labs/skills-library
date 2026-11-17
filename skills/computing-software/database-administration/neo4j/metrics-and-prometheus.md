---
id: computing-software.database-administration.neo4j.metrics-and-prometheus
name: metrics-and-prometheus
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, metrics-enable, prometheus-endpoint, page-cache-hits, neo4j-metrics, query-log, jmx, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Metrics export"
sources:
  - https://neo4j.com/docs/operations-manual/current/monitoring/metrics/expose/
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metrics and Prometheus

Goal: expose server metrics.
- Enable `server.metrics.prometheus.enabled` and set `server.metrics.prometheus.endpoint`; scrape that endpoint.
- Choose alert metrics from the metrics reference page for your version.
Verify: dashboards show live values.

## Checked

2026-11-02. Confirmed in the configuration settings reference (both prometheus settings exist). Removed: the metric list and alert suggestions (specific metric names not confirmed).
Method: documentation only; no commands were run.
