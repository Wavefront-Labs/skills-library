---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-tracing
name: grafana-mimir-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [tracing, opentelemetry, otlp, jaeger, sampling]
level: practitioner
status: docs-checked
description: "Describes configuring Mimir distributed tracing through OpenTelemetry environment variables, exporter and sampler options, with Jaeger compatibility."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-tracing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mimir tracing

Mimir supports distributed tracing with OpenTelemetry and keeps backward compatibility with Jaeger. It detects the method from the environment variables you set. OpenTelemetry is recommended.

## Backend

Any OTLP-compatible backend (Jaeger, Tempo, cloud services). For legacy Jaeger format deploy Jaeger all-in-one or agents, collectors and queriers.

## OpenTelemetry variables

- `OTEL_EXPORTER_OTLP_ENDPOINT`, for example `http://otlp-endpoint:4318`.
- `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`: traces-specific URL, overrides the above, for example `http://tempo:4318/v1/traces`.
- `OTEL_TRACES_EXPORTER`: `otlp` (default) or `none` (propagate context without exporting). The `jaeger` exporter is not available; use `otlp` since Jaeger ingests OTLP natively.
- `OTEL_TRACES_SAMPLER`: `always_on`, `always_off`, `traceidratio`, `parentbased_always_on` (default), `parentbased_always_off`, `parentbased_traceidratio`, `jaeger_remote`, `parentbased_jaeger_remote`.

The two Jaeger remote samplers also require `OTEL_TRACES_SAMPLER_ARG`, in the form `endpoint=http://localhost:14250,pollingIntervalMs=5000,initialSamplingRate=0.25`.

## Checked

2026-11-04. Confirmed against the Mimir page "Configure Grafana Mimir tracing": variables, exporter and sampler values with defaults, Jaeger exporter note, `OTEL_TRACES_SAMPLER_ARG` format. Removed the closing tip about environment placement and sampling rate (not on the page).
Method: documentation only; no commands were run.
