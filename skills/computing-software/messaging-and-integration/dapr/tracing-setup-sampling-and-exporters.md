---
id: computing-software.messaging-and-integration.dapr.tracing-setup-sampling-and-exporters
name: tracing-setup-sampling-and-exporters
category: computing-software
field: messaging-and-integration
product: dapr
tags: [tracing, opentelemetry, otel, zipkin, samplingrate, configuration, otlp, observability]
level: practitioner
status: docs-checked
description: "Enable Dapr distributed tracing: the tracing config block, probabilistic sampling default 0.0001, OTEL or Zipkin endpoints, and OTEL_EXPORTER_OTLP environment variables."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/observability/tracing/setup-tracing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tracing is recommended for any production scenario. Configure it in a Configuration file (self-hosted) or Configuration object (Kubernetes):

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing
spec:
  tracing:
    samplingRate: "1"
    otel:
      endpointAddress: "localhost:4317"
      isSecure: false
      protocol: grpc 
```

Properties: `samplingRate` (string), `stdout` (bool, more verbose trace output), `otel.endpointAddress` (hostname and optional port; if used, no `zipkin` section is needed), `otel.isSecure`, `otel.protocol` (`http` or `grpc`), `zipkin.endpointAddress` (a URL; if used, no `otel` section is needed).

Sampling is probabilistic. The value is the probability a span is sampled, from 0 to 1 inclusive. Default is 0.0001 (1 in 10,000 spans); `"1"` samples every span. `samplingRate: 0` disables tracing entirely.

The OTEL endpoint can come from the environment instead, and its presence turns tracing on for the sidecar:

- `OTEL_EXPORTER_OTLP_ENDPOINT`: server hostname and optional port.
- `OTEL_EXPORTER_OTLP_INSECURE`: true or false for an unencrypted connection.
- `OTEL_EXPORTER_OTLP_PROTOCOL`: `grpc`, `http/protobuf` or `http/json`.

The page's next steps list the OTEL Collector, New Relic, Jaeger, Zipkin, Datadog and Dash0.

## Checked

2026-11-04. Property table, example Configuration, sampling note and environment variables confirmed on the Configure Dapr to send distributed tracing data page.

Method: documentation only; no commands were run.
