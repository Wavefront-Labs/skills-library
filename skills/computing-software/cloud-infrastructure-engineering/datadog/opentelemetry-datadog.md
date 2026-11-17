---
id: computing-software.cloud-infrastructure-engineering.datadog.opentelemetry-datadog
name: opentelemetry-datadog
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, opentelemetry, otel-collector, otlp, datadog-exporter]
level: practitioner
status: docs-checked
description: "Send OTLP traces, metrics and logs to Datadog via the Agent OTLP ingest or the Collector Datadog exporter."
sources: ["https://docs.datadoghq.com/opentelemetry/otlp_ingest_in_the_agent/", "https://docs.datadoghq.com/opentelemetry/setup/collector_exporter/", "https://docs.datadoghq.com/opentelemetry/collector_exporter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry with Datadog
Goal: use OpenTelemetry instrumentation with Datadog.

Path 1, OTLP ingest in the Datadog Agent (`datadog.yaml`):

```yaml
otlp_config:
  receiver:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
  logs:
    enabled: false
```

Path 2, Collector with the Datadog exporter (fragment of the docs example):

```yaml
exporters:
  datadog/exporter:
    api:
      site: datadoghq.com
      key: ${env:DD_API_KEY}
```

- Agent OTLP ingest accepts traces and metrics over gRPC or HTTP from Agent 6.32.0 / 7.32.0, and logs from 6.48.0 / 7.48.0. It is off by default; for HTTP use `protocols.http.endpoint: 0.0.0.0:4318`. Environment equivalents: `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_GRPC_ENDPOINT` and `DD_OTLP_CONFIG_RECEIVER_PROTOCOLS_HTTP_ENDPOINT`.
- Metrics and traces ingestion is on once enabled; logs ingestion is off by default (to avoid unexpected log billing) and is turned on with `otlp_config.logs.enabled: true` or `DD_OTLP_CONFIG_LOGS_ENABLED=true`.
- The application must set `OTEL_EXPORTER_OTLP_ENDPOINT` to point at the Agent (for example `http://<datadog-agent>:4318`); the receiver alone sends nothing. Some libraries expect the `/v1/traces` path, others the root path.
- In Docker, expose the receiver port on the Agent container. The docs list a known issue where Agent 7.61.0 OTLP pipelines can fail to start in Docker.
- Collector path: the docs example uses the Datadog Exporter plus Datadog Connector, with the `hostmetrics` receiver "required to get correct infrastructure metrics in Datadog". Datadog now recommends the OTLP HTTP exporter and `span_metrics` connector for new Collector configurations; existing Datadog Exporter setups remain supported.
- Unified service tagging: set `service.name`, `deployment.environment.name` and `service.version` resource attributes on the application.
- For Datadog Exporter 0.83.0 and later, log `service` comes from `service.name`, which is not a default service attribute in Datadog log preprocessing; add a log service remapper to populate `service`.

Gotcha: the Agent and a Collector are separate paths; follow one documented setup per host rather than layering both.

## Verify
- Services from the instrumented application appear in APM, and the Agent or Collector logs show no export errors.

## Checked
2026-11-09. Confirmed against the OTLP Ingest in the Agent and Datadog Exporter pages (versions, config keys, env variables, logs default and billing note, application endpoint variable, Docker known issue, hostmetrics note, recommendation for new Collector configs, unified tagging attributes, log service remap). Removed: the invented Collector pipeline YAML with `datadog` exporter name and batch processor (docs name it `datadog/exporter`), the `deployment.environment` attribute name (docs say `deployment.environment.name`), the duplicate-host-metrics claim, "exporter options differ by Collector version", and the sampling, semantic-convention and native-tracer comparison advice.
Method: documentation only; no commands were run.
