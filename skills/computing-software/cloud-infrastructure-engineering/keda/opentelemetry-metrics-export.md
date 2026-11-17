---
id: computing-software.cloud-infrastructure-engineering.keda.opentelemetry-metrics-export
name: opentelemetry-metrics-export
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [opentelemetry, otlp, enable-opentelemetry-metrics, otel-exporter-otlp-endpoint, otel-exporter-otlp-protocol, keda-metrics]
level: advanced
status: docs-checked
description: "Push KEDA operator metrics to an OpenTelemetry Collector with --enable-opentelemetry-metrics and OTLP environment variables (experimental, v2.12+)."
sources:
  - https://keda.sh/docs/2.17/integrations/opentelemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The example sits next to `command: - /keda` and image `ghcr.io/kedacore/keda:latest`, and its endpoint uses port 4318 on a collector service in the default namespace.
Available from KEDA v2.12 and marked experimental, the operator can push metrics to an OpenTelemetry Collector. Enable it with the argument `--enable-opentelemetry-metrics=true` on the operator. KEDA pushes to the collector given by the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable, and `OTEL_EXPORTER_OTLP_PROTOCOL` picks an HTTP or gRPC client. Other standard OpenTelemetry OTLP exporter variables are supported as well.

Example operator container fragment:

```yaml
args:
  --enable-opentelemetry-metrics=true
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://opentelemetry-collector.default.svc.cluster.local:4318"
```

Metric names use dots instead of the Prometheus underscores, for example `keda.scaler.active` (1 active, 0 inactive), `keda.scaled.object.paused`, `keda.scaler.metrics.value`, `keda.scaler.metrics.latency.seconds`, `keda.scaler.errors`, `keda.scaler.errors.total`, `keda.scaled.object.errors`, `keda.scaled.job.errors`, `keda.resource.registered.count`, `keda.trigger.registered.count`, `keda.internal.scale.loop.latency.seconds`, `keda.cloudeventsource.events.emitted.count`, `keda.cloudeventsource.events.queued` and `keda.build.info`.

Deprecated names that were slated for removal in v2.16: `keda.scaler.metrics.latency`, `keda.resource.totals`, `keda.trigger.totals` and `keda.internal.scale.loop.latency` (reported in milliseconds, unlike the new seconds metric).

## Checked

2026-11-03. Confirmed on the 2.17 OpenTelemetry integration page: v2.12 availability, experimental, flag and variables, metric names, deprecated names. Removed: unsupported dashboard advice.

Method: documentation only; no commands were run.
