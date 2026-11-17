---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.prometheus-metrics-and-tracing
name: prometheus-metrics-and-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [prometheus, metrics, opentelemetry, distributed-tracing, http-request-duration]
level: practitioner
status: docs-checked
description: "Scrape OPA's /metrics endpoint with Prometheus, read http_request_duration_seconds, and export OpenTelemetry spans with exclude_paths and decision IDs."
sources:
  - https://www.openpolicyagent.org/docs/monitoring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: observe an OPA server's latency and resource use.

Prometheus: the `/metrics` endpoint is enabled by default when OPA runs as a server. Scrape config:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
- job_name: "opa"
  metrics_path: "/metrics"
  static_configs:
  - targets:
    - "localhost:8181"
```

The endpoint exports Go runtime metrics (`go_goroutines`, `go_memstats_heap_alloc_bytes`, `go_gc_duration_seconds` and others) plus `http_request_duration_seconds`, a histogram of request durations for every handler such as `v1/data`. Its default bucket upper bounds run from 1 microsecond (`1e-06`) to 1 second, so sub-microsecond latencies all land in the first bucket.

OpenTelemetry: when configured, OPA emits spans to a collector via gRPC.
- Each REST API request starts a span.
- If evaluation uses `http.send`, those HTTP clients emit descendant spans.
- Frequently polled endpoints such as the health check can be left out with `distributed_tracing.exclude_paths`.
- With decision logging enabled, evaluation spans carry the attribute `opa.decision_id`, linking a trace to a decision log entry.

Options are in the Configuration reference under distributed tracing.

For bundle and decision-log metrics (enabled through the status plugin), see status-prometheus-metrics.

Check: `curl http://localhost:8181/metrics`, issue one `v1/data` query, and confirm `http_request_duration_seconds_count` increments for that handler.

## Checked

2026-11-04. Confirmed against the OPA docs Monitoring page: OpenTelemetry spans over gRPC, a span per REST request, descendant spans from http.send, distributed_tracing.exclude_paths, the opa.decision_id attribute when decision logging is enabled, the Prometheus endpoint enabled by default in server mode, the scrape configuration, the Go runtime metrics and http_request_duration_seconds histogram, and the default bucket bounds from 1e-06 to 1 second. Nothing removed.

Method: documentation only; no commands were run.
