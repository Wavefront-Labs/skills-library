---
id: computing-software.cloud-infrastructure-engineering.observability.deriving-metrics-from-spans-and-logs
name: deriving-metrics-from-spans-and-logs
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [metrics-from-spans, derived-metrics-from-logs, spanmetrics-connector, metrics-generator, loki-recording-rules, observability, opentelemetry]
level: practitioner
status: docs-checked
description: "Generate RED metrics from spans (spanmetrics connector, Tempo metrics-generator) and counts from logs instead of instrumenting the same event twice."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector", "https://grafana.com/docs/tempo/latest/metrics-generator/", "https://grafana.com/docs/loki/latest/alert/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deriving metrics from spans and logs

Goal: one instrumentation point per event, with metrics computed downstream, so counters and spans never disagree.

## Decide what to derive
| Source | Derive | Do not derive |
|---|---|---|
| Server/client spans (100% before sampling) | request rate, error rate, latency histogram per service/route | business KPIs needing exact counts after sampling |
| Logs with stable fields | error counts, event counts, rare-event alerts | high-volume latency percentiles (use spans/histograms) |
| App metrics | saturation, queue depth, pool usage | per-request data |

Rule: derive **before** any sampling step. Span metrics computed after tail sampling undercount.

## Collector: spanmetrics connector
```yaml
connectors:
  spanmetrics:                 # renamed span_metrics in newer collector-contrib; old name still accepted as an alias
    histogram:
      explicit: {buckets: [5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s]}
    dimensions:
      - name: http.route
      - name: http.response.status_code
    aggregation_cardinality_limit: 1000   # replaces deprecated dimensions_cache_size
    aggregation_temporality: AGGREGATION_TEMPORALITY_CUMULATIVE
    metrics_flush_interval: 15s
service:
  pipelines:
    traces:            {receivers: [otlp], processors: [batch], exporters: [spanmetrics, otlp/tempo]}
    metrics/spanmetrics: {receivers: [spanmetrics], exporters: [prometheusremotewrite]}
```
Output: (the connector emits `traces.span.metrics.calls` and a duration histogram; the exported names vary by version and exporter, so check once).

## Tempo metrics-generator
The metrics-generator runs a set of processors (span metrics, service graphs) over ingested spans and remote-writes the result; see the Tempo page for the current processor names and per-tenant overrides. Tempo sees only traces that reached it, so place sampling after it or accept undercounting.

## Logs to metrics
- Loki ruler recording rule: `sum by (app) (count_over_time({app="api"} |= "payment failed" [1m]))` remote-written as a series (see the Loki alerting and recording rules page).
- Collector `count` connector: counts spans, span events, logs and other signals matching OTTL conditions into a metric.

## Gotchas
- Every dimension multiplies series. Never use `url.full`, user ids or trace ids as dimensions.
- `span.name` with ids in it (`GET /users/123`) explodes cardinality: fix span naming first.
- Derived and hand-written metrics for the same thing will drift; delete one.

## Verify
- [ ] Derived request rate is within ~1% of LB/ingress request counts over an hour.
- [ ] Active series added by the connector match the estimate (services x routes x status x buckets).

## Checked
Checked 2026-10-28 against the spanmetrics connector README (collector-contrib), the Tempo metrics-generator page, the Loki alert page and the Collector connector docs.
- Confirmed: `histogram.explicit.buckets`, `dimensions`, `metrics_flush_interval`, `aggregation_temporality` with `AGGREGATION_TEMPORALITY_CUMULATIVE`, the count connector, `traces.span.metrics.calls` output.
- Fixed: `dimensions_cache_size` is deprecated in favour of `aggregation_cardinality_limit`; the component type was renamed `span_metrics` (old `spanmetrics` kept as alias).
- Removed: hard-coded Prometheus-style output names and the `span-metrics`/`service-graphs` processor spelling (not on the fetched page).
- Collector v0.15x README text was read; Tempo 3.0 notes appear on the page.

Method: documentation only; no commands were run.
