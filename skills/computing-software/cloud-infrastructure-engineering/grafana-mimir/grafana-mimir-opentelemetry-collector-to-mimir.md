---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-opentelemetry-collector-to-mimir
name: grafana-mimir-opentelemetry-collector-to-mimir
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [opentelemetry, otlp, collector, remote-write, basic-auth]
level: practitioner
status: docs-checked
description: "Shows how to send metrics from the OpenTelemetry Collector to Mimir with the otlphttp exporter or Prometheus remote write, including basic authentication."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-otel-collector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenTelemetry Collector to Mimir

The Collector can write to Mimir with OTLP or Prometheus remote write.

## OTLP over HTTP

Mimir serves native OTLP over HTTP. Use the `otlphttp` exporter pointed at the `/otlp` path:

```yaml
exporters:
  otlphttp:
    endpoint: http://<mimir-endpoint>/otlp
service:
  pipelines:
    metrics:
      receivers: [...]
      processors: [...]
      exporters: [..., otlphttp]
```

## Basic authentication

Use the `basicauth` extension and reference it from the exporter:

```yaml
extensions:
  basicauth/otlp:
    client_auth:
      username: username
      password: password
exporters:
  otlphttp:
    auth:
      authenticator: basicauth/otlp
    endpoint: http://<mimir-endpoint>/otlp
service:
  extensions: [basicauth/otlp]
```

Replace the placeholder username and password with real credentials.

## Prometheus remote write

Alternatively add the `prometheusremotewrite` exporter in the exporters section and list it in the metrics pipeline. For Grafana Cloud use the Grafana Cloud OTLP instructions instead.

## Checked

Confirmed against the page: native OTLP over HTTP, `otlphttp` exporter and `/otlp` path, pipeline wiring, `basicauth` extension example, `prometheusremotewrite` alternative, Grafana Cloud pointer. Removed the unsupported environment-variable-substitution advice.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-otel-collector page (grafana/mimir main), read in full.
