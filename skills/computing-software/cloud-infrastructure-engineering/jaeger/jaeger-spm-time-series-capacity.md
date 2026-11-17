---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-spm-time-series-capacity
name: jaeger-spm-time-series-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, calls-total, duration-histogram, spanmetrics-cardinality, time-series-formula]
level: sme
status: docs-checked
description: "Estimate the time series SPM creates with num_status_codes * num_span_kinds * (1 + num_latency_buckets) * num_operations."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/spm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: plan capacity for the metrics store.

The spanmetrics connector produces two metric names:
- `calls_total` (counter): total spans including errors, separated by the `status_code` label; errors have `status_code = "STATUS_CODE_ERROR"`.
- `[namespace_]duration_[units]` (histogram), e.g. `duration_milliseconds_count`, `_sum` and `_bucket` (one series per bucket, labelled `le`).

Formula:
`num_status_codes * num_span_kinds * (1 + num_latency_buckets) * num_operations`
with num_status_codes at most 3 (typically 2), num_span_kinds at most 6 (typically 2) and num_latency_buckets 17 by default. That gives a maximum of 324 times the number of operations and a typical 72 times.

Custom duration buckets or dimensions in the connector change the result. Querying custom dimensions is not supported by SPM; they are aggregated over.

Programmatic access: gRPC `jaeger.api_v2.metrics.MetricsQueryService` (metricsquery.proto). The HTTP JSON API is used internally by the Monitor tab.

Related: the same Prometheus metric names may differ by exporter version; see the SPM troubleshooting skill for `normalize_calls` and `normalize_duration`.

## Checked

2026-11-03. Confirmed against the SPM page, Derived Time Series section: calls_total and duration histogram series, the formula and its maxima (3 status codes, 6 span kinds, 17 buckets, 324 and 72 per operation), custom dimensions not supported, and the MetricsQueryService gRPC API. Removed: a closing paragraph of unverified usage advice.
Method: documentation only; no commands were run.
