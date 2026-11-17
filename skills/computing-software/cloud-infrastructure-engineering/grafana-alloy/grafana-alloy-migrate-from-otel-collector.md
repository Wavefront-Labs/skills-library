---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-migrate-from-otel-collector
name: grafana-alloy-migrate-from-otel-collector
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [migrate-otel-collector, configformat-otelcol, otelcol-convert, service-telemetry]
level: practitioner
status: docs-checked
description: "Convert an OpenTelemetry Collector config to Alloy otelcol.* components, run it with --config.format=otelcol, and the limitations on service telemetry and env schemes."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/set-up/migrate/from-otelcol.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from the OpenTelemetry Collector

```shell
alloy convert --source-format=otelcol --output=/path/to/config.alloy /path/to/otelcol.yaml
```
The example pipeline uses `otelcol.receiver.otlp`, `otelcol.processor.memory_limiter` and `otelcol.exporter.otlp`. As with other sources, `--report` writes diagnostics, `--bypass-errors` gives best-effort output, and `alloy run --config.format=otelcol` runs the Collector file directly (with `--config.bypass-conversion-errors` as a last resort, not for production).

## Limitations
- Only components that directly embed upstream Collector features are supported; check the `otelcol.*` reference for what exists.
- Extra Collector command-line arguments not in the config file need checking.
- Meta-monitoring metrics have different names, so update alerts and dashboards; logs differ too.
- The UI uses Alloy naming for components, blocks and arguments.
- Not every argument under `service/telemetry` is supported.
- Environment variable schemes other than `env` are unsupported; a reference with no scheme defaults to `env`.

## Checked

2026-11-04. Confirmed against the Migrate from OpenTelemetry Collector page (set-up/migrate/from-otelcol.md): convert and run commands, example components, bypass flags, limitations list. No claims changed.

Method: documentation only; no commands were run.
