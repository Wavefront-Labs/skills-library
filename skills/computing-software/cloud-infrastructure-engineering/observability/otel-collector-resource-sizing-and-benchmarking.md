---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-resource-sizing-and-benchmarking
name: otel-collector-resource-sizing-and-benchmarking
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [collector-resource-sizing, collector-benchmarks, collector-deployment, otel-collector, telemetrygen]
level: advanced
status: docs-checked
description: "Size OTel Collector CPU and memory from measurements: telemetrygen load tests, key self-metrics, memory_limiter and GOMEMLIMIT settings, and headroom rules."
sources: ["https://opentelemetry.io/docs/collector/scaling/", "https://opentelemetry.io/docs/collector/benchmarks/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/cmd/telemetrygen", "https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor/memorylimiterprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector resource sizing and benchmarking

There is no fixed number: throughput per core depends heavily on processors (OTTL transforms, regex redaction, tail
sampling) and exporters (compression). The OTel project publishes load-test results on its benchmarks page; use them
for orientation, then measure your own config.

## Load test your pipeline
```bash
go install github.com/open-telemetry/opentelemetry-collector-contrib/cmd/telemetrygen@latest
telemetrygen traces --otlp-endpoint otel-gateway:4317 --otlp-insecure --rate 5000 --duration 10m \
  --otlp-attributes 'service.name="loadtest"'
telemetrygen logs --otlp-insecure --rate 20000 --duration 10m
telemetrygen metrics --otlp-insecure --rate 1000 --duration 10m
```
Run against a staging collector with the real config (exporting to a sink like another collector with `nop`
exporter, or the real backend if it can take it). Step the rate up until refusals appear.

## Watch
| Metric | Meaning |
|---|---|
| `otelcol_process_cpu_seconds` (rate) | CPU per pod |
| `otelcol_process_memory_rss` | memory (resident set size) |
| `otelcol_receiver_refused_*` | memory_limiter or downstream pushback |
| `otelcol_exporter_queue_size` / `otelcol_exporter_queue_capacity` | backend keeping up? |

## Settings
```yaml
processors:
  memory_limiter:
    check_interval: 1s
    limit_percentage: 80
    spike_limit_percentage: 25
```
plus env `GOMEMLIMIT` ~ 80% of the container memory limit. memory_limiter must be the
first processor in every pipeline.

## Headroom rules
- Size for peak plus headroom (deploys, incident traffic, retries after a backend outage).
- Requests = typical usage so the scheduler packs correctly; limits = peak with headroom.
- Sending queue memory = queue_size x batch size x item size - include it in memory sizing.
- Tail sampling buffers whole traces in memory; measure it under your real trace shapes.

## Verify
At target peak: CPU comfortably below the limit, zero refused, exporter queue well below capacity, and no restarts over a long soak.

## Checked
- 2026-10-28. Checked against the Collector internal-telemetry, scaling and troubleshooting pages, telemetrygen README (`go install ...telemetrygen@latest`, `--otlp-attributes`, `--rate`, `--duration`, `--otlp-insecure`) and memorylimiterprocessor README (collector main, 2026-10).
- Confirmed: `otelcol_process_cpu_seconds`, `otelcol_process_memory_rss`, `otelcol_exporter_queue_size`/`_capacity`, `otelcol_receiver_refused_*`, `check_interval`, `limit_percentage`, `spike_limit_percentage`, `GOMEMLIMIT` 80 %, memory_limiter first.
- Removed (unconfirmed): `--workers`, `--child-spans`, heap-alloc metric, batch_send_size metric, Helm `useGOMEMLIMIT`, "nightly" benchmarks, the 1.5-2x, 70 % and 20 % rules of thumb, tail-sampling memory formula.
Method: documentation only; no commands were run.
