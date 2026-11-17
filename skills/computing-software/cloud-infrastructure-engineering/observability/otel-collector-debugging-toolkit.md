---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-debugging-toolkit
name: otel-collector-debugging-toolkit
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-troubleshooting, service-telemetry-config, internal-telemetry-level, internal-telemetry-otlp, telemetrygen-usage, synthetic-otlp-data, collector-alert-rules, collector-dropped-data-alerts, zpages-usage, tracez, otelcol-validate, config-dry-run, collector-oom, memory-ballast-limits, feature-gates, collector-feature-gates]
level: advanced
status: docs-checked
description: "Debug an OTel Collector: internal telemetry levels and OTLP export, telemetrygen load, zPages, otelcol validate, feature gates, OOM tuning, and alert rules on dropped data."
sources: ["https://opentelemetry.io/docs/collector/internal-telemetry/", "https://opentelemetry.io/docs/collector/troubleshooting/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen", "https://github.com/open-telemetry/opentelemetry-collector/blob/main/extension/zpagesextension/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector debugging toolkit

## Internal telemetry
```yaml
service:
  telemetry:
    logs: {level: info}                    # debug only temporarily
    metrics:
      level: detailed                      # none | basic | normal | detailed
      readers:
        - pull: {exporter: {prometheus: {host: 0.0.0.0, port: 8888}}}
        - periodic: {exporter: {otlp: {protocol: grpc, endpoint: http://otel-self-monitoring:4317}}}
```
Send internal telemetry to a **different** pipeline/backend than the one being debugged.

## Alert rules on collector health
```yaml
- alert: OtelExporterFailing
  expr: sum by (exporter) (rate(otelcol_exporter_send_failed_spans_total[5m]) + rate(otelcol_exporter_send_failed_metric_points_total[5m]) + rate(otelcol_exporter_send_failed_log_records_total[5m])) > 0
  for: 10m
- alert: OtelQueueNearlyFull
  expr: otelcol_exporter_queue_size / otelcol_exporter_queue_capacity > 0.8
  for: 5m
- alert: OtelReceiverRefusing
  expr: sum by (receiver) (rate(otelcol_receiver_refused_spans_total[5m])) > 0
  for: 5m
```
(Metric names gained `_total` and moved between versions; check `curl :8888/metrics | grep otelcol_` on yours.)

## Generate test data
```bash
telemetrygen traces --otlp-endpoint=otel-collector:4317 --otlp-insecure --rate=200 --duration=60s --service=probe
telemetrygen metrics --otlp-endpoint=otel-collector:4317 --otlp-insecure --metrics=50
telemetrygen logs --otlp-endpoint=otel-collector:4317 --otlp-insecure --logs=1000
```
Then confirm arrival with the `debug` exporter (`verbosity: detailed`) or in the backend.

## zPages
`extensions: [zpages]` (`endpoint: 0.0.0.0:55679`): `/debug/tracez` (sampled internal spans, errors and latency
buckets per component), `/debug/pipelinez` (pipeline layout), `/debug/extensionz`, `/debug/featurez`.

## Validate and dry run
```bash
otelcol-contrib validate --config=config.yaml        # parses, checks components exist and pipelines are wired
otelcol-contrib components                            # list built-in components of this distribution
```
`validate` doesn't test connectivity; follow with telemetrygen against a staging instance.

## Feature gates
`--feature-gates=+gate.id,-other.gate`. List gates on the `/debug/featurez` zPage or in the release notes, and read each gate's stage in its description.

## OOM
- Symptoms: restarts with OOMKilled, gaps. Fix order: `memory_limiter` first in each pipeline with
  `limit_percentage` 75-80; `GOMEMLIMIT` ~80 % of container limit;
  reduce `batch` sizes, tail-sampling buffers, `sending_queue.queue_size`; scale out.
- gRPC/TLS errors: `transport: authentication handshake failed` = TLS mismatch (`insecure: true` vs TLS endpoint);
  `connection refused` on 4317 = wrong protocol/port (HTTP is 4318).

## Verify
- [ ] Self-monitoring dashboard shows accepted vs sent per signal roughly equal.
- [ ] telemetrygen run end to end produces data in the backend.

## Checked
- 2026-10-28. Checked against the Collector internal-telemetry and troubleshooting pages, the zpagesextension README, memorylimiterprocessor README and telemetrygen README (collector main, 2026-10).
- Confirmed: internal metric names (`otelcol_exporter_queue_size`, `_queue_capacity`, `send_failed_*`, `receiver_refused_spans`), zPages port 55679 and `/debug/tracez`, `GOMEMLIMIT` 80 %, `limit_percentage`, `verbosity: detailed`, telemetrygen flags.
- Removed (unconfirmed): `--body`, memory-ballast claim, `num_traces`, alpha/beta gate defaults.
Method: documentation only; no commands were run.
