---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.tail-sampling-with-alloy-before-tempo
name: tail-sampling-with-alloy-before-tempo
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [tail-sampling, tempo, otelcol-processor-tail-sampling, sampling-policies, loadbalancing-exporter, trace-completeness]
level: practitioner
status: docs-checked
description: "Reduce trace volume with Alloy tail sampling in front of Tempo: policy order, decision period, caches, trace-ID load balancing and where to generate metrics."
sources: ["https://grafana.com/docs/tempo/latest/set-up-for-tracing/instrument-send/set-up-collector/tail-sampling/", "https://grafana.com/docs/tempo/latest/set-up-for-tracing/instrument-send/set-up-collector/tail-sampling/policies-strategies/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/where-to-generate-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store the interesting traces only, without breaking metrics or trace completeness.

Alloy's `otelcol.processor.tail_sampling` wraps the OpenTelemetry tail sampling processor. It groups spans by trace ID, waits a decision period, and keeps a trace when it meets at least one policy. Example with error, latency and a baseline (put the catch-all last):
```alloy
otelcol.processor.tail_sampling "default" {
  decision_wait = "30s"
  policy {
    name = "errors"
    type = "status_code"
    status_code { status_codes = ["ERROR"] }
  }
  policy {
    name = "slow"
    type = "latency"
    latency { threshold_ms = 5000 }
  }
  policy {
    name = "baseline"
    type = "probabilistic"
    probabilistic { sampling_percentage = 10 }
  }
  output { traces = [otelcol.exporter.otlp.tempo.input] }
}
otelcol.exporter.otlp "tempo" {
  client { endpoint = "http://tempo:4318" }
}
```
Policy types: `always_sample`, `and`, `boolean_attribute`, `composite`, `latency` (with `threshold_ms`, optional `max_duration_ms`), `numeric_attribute`, `ottl_condition`, `probabilistic`, `rate_limiting`, `span_count`, `status_code`, `string_attribute`, `trace_state`.

Order matters: policies run in the order defined and evaluation stops at the first match. A probabilistic policy placed first would sample 10% and stop, throwing away errors and slow traces. Common targets: drop health-check traces, keep errors and high latency, sample a baseline of 1% or fewer.

Decision period: spans older than `decision_wait` get a new decision, so a long trace can be stored fragmented. Longer waits cost memory. The sampled and non-sampled caches (each sized by a maximum trace count, enable independently or both) make earlier decisions stick after the period; both caches together lower memory but can lose spans of long traces.

Load balancing: all spans of a trace must reach one sampling instance. Use two collector layers: layer one routes with the load-balancing exporter (`otelcol.exporter.loadbalancing`, routing key usually `traceID`; static, DNS A-record or Kubernetes headless service targets), layer two samples. The docs suggest a StatefulSet for layer two. Routing is eventually consistent while the backend set changes.

Metrics: sampling does not reduce what services produced. If you tail sample before Tempo, generate span metrics and service graphs in the collector with the span metrics and servicegraph connectors placed before the sampler, and avoid running a second generator in Tempo (duplicate series). If traces reach Tempo unsampled, use Tempo's metrics-generator. Transform processors must come before connectors and the sampler.

Gotchas
- Dropped traces still appear in log trace IDs and exemplars; the link then fails to find the trace.
- Policy order is first-match, not an unordered OR.

## Verify
Confirm Tempo receives only the intended traces (errors and slow ones present, baseline fraction near its percentage) and that collector-generated RED metrics still match total traffic.

## Checked
2026-11-03. Confirmed against the Tempo Sampling page, the policies and strategies page and the where-to-generate-metrics page. Removed: `num_traces`, the `otelcol_processor_tail_sampling_*` metric names and Alloy curl check (not on those pages), `routing_key` snippet, the "decision_wait must exceed typical trace duration" absolute wording, and the "Multiple policies are OR'd" claim, replaced by first-match order.
Method: documentation only; no commands were run.
