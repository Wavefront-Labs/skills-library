---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-spm-troubleshooting
name: jaeger-spm-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-metricstore-requests-total, normalize-calls, token-file-path, span-kind]
level: sme
status: docs-checked
description: "Debug an empty Monitor tab: jaeger_metricstore counters, metric name normalization, status.code dimensions and 403 errors."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/spm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find why SPM graphs are empty.

1. Connectivity: expose internal telemetry on a port different from the spanmetrics exporter (8888 versus 8889) with `service.telemetry.metrics` (`level: detailed`, `address: 0.0.0.0:8888`), then `curl -s http://jaeger:8888/metrics | grep jaeger_metricstore`. Watch `jaeger_metricstore_requests_total` and `jaeger_metricstore_latency_bucket` for operations get_call_rates, get_error_rates, get_latencies and get_min_step_duration. `result="ok"` should climb; `result="err"` rising means Prometheus read failures.
2. Query Prometheus directly for `traces_span_metrics_duration_milliseconds_bucket` and `traces_span_metrics_calls_total`; they should increase.
3. Set `service.telemetry.logs.level: debug` and read the logged Prometheus queries. If the exporter writes `calls_total` and `duration_milliseconds_bucket` but Jaeger looks for others, set `normalize_calls: true` and `normalize_duration: true` on the prometheus metric backend.
4. Error spans present but no error metrics: check the `status.code` label exists; look for `exclude_dimensions: ['status.code']` in the collector config.
5. Service missing in Monitor but visible in search: the metrics queries default to server span kind; fix instrumentation to set span kind.
6. 403 (`failed executing metrics query: client_error: client error: 403`): the server expects a bearer token; set `token_file_path` on the prometheus backend.

## Checked

2026-11-03. Confirmed against the SPM page, Troubleshooting section: separate telemetry port, the jaeger_metricstore metrics and operation labels, ok versus err results, the traces_span_metrics_* names, debug logging, normalize_calls and normalize_duration, the status.code and exclude_dimensions check, server span kind default and the 403 bearer token fix with token_file_path. Nothing removed.
Method: documentation only; no commands were run.
