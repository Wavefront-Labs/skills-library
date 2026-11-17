---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-spm-prometheus-setup
name: jaeger-spm-prometheus-setup
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, spm, spanmetrics-connector, metrics-storage, monitor-menu-enabled]
level: sme
status: docs-checked
description: "Enable the Monitor tab with the spanmetrics connector feeding a PromQL-compatible store referenced from jaeger_query."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/spm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: show RED metrics (rate, errors, duration) in the UI.

SPM aggregates span data into RED metrics per service and per operation (P95, P75, P50 durations, plus an Impact metric: latency times request rate). Steps (config-spm.yaml is the example):
1. Add a prometheus exporter, the spanmetrics connector, and bridge pipelines:
```
exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
connectors:
  spanmetrics:
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger_storage_exporter, spanmetrics]
    metrics/spanmetrics:
      receivers: [spanmetrics]
      exporters: [prometheus]
```
2. Define a PromQL backend under `metric_backends:` in `jaeger_storage` (for example `prometheus` with `endpoint: http://prometheus:9090`).
3. Reference it in `jaeger_query` (`storage.metrics`).
4. Set `monitor.menuEnabled=true` in the UI config.

Prometheus must scrape the exporter endpoint (or use a push exporter). Any PromQL-compatible store works. The default span kind in queries is server, to avoid double counting ingress and egress spans.

Alternative: with Elasticsearch or OpenSearch, point `storage.traces` and `storage.metrics` at the same backend; no spanmetrics connector or metrics pipeline is needed (config-spm-elasticsearch.yaml).

## Checked

2026-11-03. Confirmed against the SPM page: RED metrics and the Impact metric, the spanmetrics connector and prometheus exporter pipeline, metric_backends, jaeger_query metrics reference, monitor.menuEnabled, the PromQL-compatible and push-exporter notes, the server span kind default and the Elasticsearch/OpenSearch alternative. Nothing removed.
Method: documentation only; no commands were run.
