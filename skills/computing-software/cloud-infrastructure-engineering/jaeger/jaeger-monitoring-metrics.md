---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-monitoring-metrics
name: jaeger-monitoring-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, otelcol-receiver-accepted-spans, internal-telemetry, port-8888, prometheus-scrape]
level: practitioner
status: docs-checked
description: "Scrape the Jaeger internal metrics on 8888 and compare accepted versus sent spans to spot data loss."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: monitor ingestion health.

Fetch metrics: `curl -s http://jaeger-collector:8888/metrics`

Key counters:
- `otelcol_receiver_accepted_spans`
- `otelcol_receiver_refused_spans` (indicates data loss)
- `otelcol_exporter_sent_spans`
- `otelcol_exporter_send_failed_spans`

The first two show spans received; the last two show spans sent to storage. Under normal conditions accepted and sent should be close. Labels separate receivers and exporters, for example `otelcol_receiver_accepted_spans{receiver="otlp",service_name="jaeger",transport="http"}`.

Prometheus scrape config:
```
scrape_configs:
  - job_name: 'jaeger-v2'
    static_configs:
      - targets: ['jaeger:8888']
    scrape_interval: 15s
    metrics_path: /metrics
```
Also watch CPU, RSS and virtual memory, file descriptors, network I/O, disk usage and I/O for components with local storage, and Go runtime metrics (GC pauses and frequency, goroutine count and growth, heap use). The Jaeger repository includes sample Prometheus alerting rules (availability, latency and errors, resource exhaustion and queue saturation, dropped spans and storage failures); setup is in the monitoring mixin documentation. Internal telemetry configuration follows the OpenTelemetry Collector docs.

Troubleshooting pointers from the same page: for data loss (refused or failed spans) check storage backend health and connectivity, verify exporter configuration and review receiver capacity; for high resource usage check goroutine counts and memory patterns and review the collector configuration; for poor query performance check the storage backend and resource contention.

## Checked

2026-11-03. Confirmed against the Monitoring page: the curl command, the four otelcol counters and their meaning, label example, the Prometheus scrape config, the process, Go runtime and query metrics lists, the sample alert rules and mixin, and the troubleshooting pointers. Nothing removed.
Method: documentation only; no commands were run.
