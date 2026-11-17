---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-collect-opentelemetry-otlp
name: grafana-alloy-collect-opentelemetry-otlp
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [otelcolexporterotlp, otelcolexporterotlphttp, otelcolauthbasic, otlp-ports-4317-4318, otelcol-pipeline, memory-limiter-chain]
level: practitioner
status: docs-checked
description: "Build an Alloy OTLP pipeline: receiver on 4317 and 4318, memory_limiter and batch processors, an authenticated otelcol.exporter.otlp, and otlphttp for HTTP/1.1."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/collect/opentelemetry-data.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collecting and forwarding OpenTelemetry data

Receivers, processors and exporters connect through `output` blocks and `.input` exports.

```alloy
otelcol.receiver.otlp "example" {
  grpc { endpoint = "127.0.0.1:4317" }
  http { endpoint = "127.0.0.1:4318" }
  output {
    metrics = [otelcol.processor.memory_limiter.default.input]
    logs    = [otelcol.processor.memory_limiter.default.input]
    traces  = [otelcol.processor.memory_limiter.default.input]
  }
}
otelcol.processor.memory_limiter "default" {
  check_interval = "1s"
  limit          = "1GiB"
  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}
otelcol.processor.batch "default" {
  output {
    metrics = [otelcol.exporter.otlp.default.input]
    logs    = [otelcol.exporter.otlp.default.input]
    traces  = [otelcol.exporter.otlp.default.input]
  }
}
otelcol.exporter.otlp "default" {
  client {
    endpoint = "my-otlp-grpc-server:4317"
    auth     = otelcol.auth.basic.credentials.handler
  }
}
otelcol.auth.basic "credentials" {
  username = sys.env("BASIC_AUTH_USER")
  password = sys.env("API_KEY")
}
```

## Notes
- gRPC listens on 4317, HTTP on 4318; use `0.0.0.0` to listen on all interfaces. The examples use `127.0.0.1`.
- Disable a signal by setting its output list to `[]`, for example `metrics = []`.
- `otelcol.exporter.otlp` sends OTLP over gRPC (HTTP/2); use `otelcol.exporter.otlphttp` for HTTP/1.1 servers.
- Production configs should batch rather than send straight to the exporter; batching improves compression and cuts request count. Processors chain by pointing one `output` at the next processor's `.input`.
- Auth components attach via `auth = otelcol.auth.basic.LABEL.handler` in the `client` block.

## Checked

2026-11-04. Confirmed against the Collect OpenTelemetry data page (collect/opentelemetry-data.md): receiver, processor, exporter and auth wiring, ports 4317 and 4318, gRPC vs HTTP/1.1 exporter note, batching and empty-list notes. No claims changed.

Method: documentation only; no commands were run.
