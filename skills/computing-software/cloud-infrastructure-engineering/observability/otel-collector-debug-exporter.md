---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-debug-exporter
name: otel-collector-debug-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [debug-exporter-verbosity, debug-exporter, collector-troubleshooting, otel-collector, logging-exporter]
level: practitioner
status: docs-checked
description: "Inspect what flows through a collector pipeline with the debug exporter: verbosity levels, sampling to limit log volume, and safe use alongside real exporters."
sources: ["https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/debugexporter", "https://opentelemetry.io/docs/collector/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug exporter

Outputs telemetry to the console for debugging, through the collector's internal logger by default. Stability: alpha, and the README warns the output format is unstable, so do not parse it.

```yaml
exporters:
  debug:
    verbosity: detailed          # basic (default) | normal | detailed
    sampling_initial: 5          # messages logged each second before sampling (default 2)
    sampling_thereafter: 200     # then every Mth message (default 1 = sampling off)
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, transform, batch]
      exporters: [otlp/tempo, debug]   # tee: real exporter plus debug
```
| verbosity | Output |
|---|---|
| `basic` | one-line summary with record counts for every batch |
| `normal` | about one line per telemetry record (multiline log bodies span several lines) |
| `detailed` | all details of every record, typically several lines each (resource attributes, scope, span fields, attributes) |

## Workflow
1. Add `debug` to the suspect pipeline with `detailed` and tight sampling.
2. Send a known test item through the pipeline.
3. Read the collector's log output; with `detailed` each batch starts with a `ResourceSpans #0` style header.
4. To see before/after a processor, add a second pipeline (via a forward connector) or temporarily remove processors.
5. Remove the debug exporter afterwards.

## Gotchas
- Detailed output at production volume floods logs; set `sampling_initial` and `sampling_thereafter` so only a sample is printed.
- With `use_internal_logger: false` (default true) the output ignores `service::telemetry::logs` and goes to `output_paths` (default `["stdout"]`).
- Logs may contain sensitive attributes; do not leave debug output shipping to a shared log system.

## Verify
- [ ] The item's attributes in the debug dump match what the backend shows (or reveal where they change).

## Checked

2026-10-24. OpenTelemetry Collector debug exporter README (main branch). Confirmed: `verbosity` values and default (`basic`), `sampling_initial` default 2, `sampling_thereafter` default 1 (disabled), `use_internal_logger` and `output_paths`, alpha stability and the unstable output format warning, and the output shape per verbosity level. Removed the unconfirmed claim about the deprecated `logging` exporter.

Method: documentation only; no commands were run.
