---
id: computing-software.search-and-information-retrieval.apache-solr.metrics-prometheus-otel
name: metrics-prometheus-otel
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [metrics, prometheus, opentelemetry, monitoring, metrics-endpoint]
level: practitioner
status: docs-checked
description: "Monitor Solr with its metrics: the Prometheus-format /metrics endpoint, wt=prometheus or openmetrics, OTLP push export and the metric registries."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/metrics-reporting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# metrics-prometheus-otel

Solr exposes a pull-based Prometheus-formatted API and an OTLP push exporter, built on OpenTelemetry instruments. Metrics are raw data (counters, histograms); the monitoring backend such as Prometheus or Grafana aggregates them and computes rates and averages.

The `/metrics` endpoint serves all metrics in Prometheus format by default. Use `wt=prometheus` or `wt=openmetrics` to choose the format. The V2 `/metrics` endpoint equals V1 `/admin/metrics`. The guide marks the Solr 10 metrics as Beta, so names and endpoints may change in minor releases.

Registries:
- Node (CoreContainer): process-level metrics, prefixed `solr_node_`.
- Core (SolrCore): one per core, prefixed `solr_core_`, with standard labels such as the core or collection.
- JVM: via OpenTelemetry instrumentation with JFR and JMX; also a gauge for host or container physical memory.
- Overseer: present in SolrCloud mode.
- HTTP client registry.

Metric names for each registry are tabulated on the page. Build alerts from the derived rates, not from single raw counter values.

## Checked

Checked 2026-11-09 against the Metrics Reporting page of the Solr Reference Guide: introduction, registries (node, core, JVM, Overseer, HTTP client), Metrics API and OTLP sections. Removed the `metrics-read` permission claim, which is not on that page. The per-registry metric tables were not read in full.

Method: docs-checked 2026-11-09 against the Metrics Reporting page (raw ref-guide source); no commands were run.
