---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-opentelemetry-collector-pipeline
name: alloy-opentelemetry-collector-pipeline
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [alloy-otelcol, alloy, otelcol.receiver.otlp, otelcol.processor.batch, otelcol.exporter.otlp, otelcol.exporter.loki, otlp-pipeline]
level: practitioner
status: draft
description: "Build an OpenTelemetry pipeline in Alloy - OTLP receiver, batch and memory limiter, exporters to Tempo, Mimir and Loki."
sources: ["https://grafana.com/docs/alloy/latest/reference/components/otelcol/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: one agent receiving OTLP and fanning out to the LGTM backends.

```
otelcol.receiver.otlp "default" {
  grpc { endpoint = "0.0.0.0:4317" }
  http { endpoint = "0.0.0.0:4318" }
  output {
    metrics = [otelcol.processor.memory_limiter.default.input]
    logs    = [otelcol.processor.memory_limiter.default.input]
    traces  = [otelcol.processor.memory_limiter.default.input]
  }
}

otelcol.processor.memory_limiter "default" {
  check_interval = "1s"
  limit          = "512MiB"
  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}

otelcol.processor.batch "default" {
  output {
    metrics = [otelcol.exporter.otlphttp.mimir.input]
    logs    = [otelcol.exporter.otlphttp.loki.input]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}

otelcol.exporter.otlp "tempo" {
  client { endpoint = "tempo:4317"  tls { insecure = true } }
}
otelcol.exporter.otlphttp "mimir" { client { endpoint = "http://mimir:9009/otlp" } }
otelcol.exporter.otlphttp "loki"  { client { endpoint = "http://loki:3100/otlp" } }
```
Gotchas
- Put `memory_limiter` first and `batch` last before exporters.
- Loki's OTLP endpoint is `/otlp`; the exporter adds `/v1/logs`.
- `insecure` TLS only inside trusted networks.
- Hyphens in attribute names become underscores in Loki labels.

## Verify
Send a test span with `telemetrygen traces --otlp-insecure --traces 5`; the component page shows accepted spans and Tempo search finds them.
