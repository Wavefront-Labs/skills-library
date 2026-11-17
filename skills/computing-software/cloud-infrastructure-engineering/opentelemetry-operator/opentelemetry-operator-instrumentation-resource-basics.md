---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-resource-basics
name: opentelemetry-operator-instrumentation-resource-basics
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, instrumentation, otelinst, propagators, sampler, otel-exporter-otlp-endpoint]
level: intro
status: docs-checked
description: "Define an Instrumentation resource with exporter endpoint, propagators and sampler, and know which env vars it sets and why Python, .NET and Go need port 4318."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/instrumentations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The Instrumentation resource

Supported languages: Apache HTTPD, DotNet, Go, Java, Nginx, NodeJS, PHP, Python and Ruby. The resource is `Instrumentation` (apiVersion `opentelemetry.io/v1alpha1`), queryable with `kubectl get otelinst`.

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: my-instrumentation
spec:
  exporter:
    endpoint: http://otel-collector:4317
  propagators: [tracecontext, baggage, b3]
  sampler:
    type: parentbased_traceidratio
    argument: "0.25"
  python:
    env:
      - name: OTEL_EXPORTER_OTLP_ENDPOINT
        value: http://otel-collector:4318
```

Mapping to SDK environment variables:
- `propagators` values go to `OTEL_PROPAGATORS` (enum: tracecontext, baggage, b3, b3multi, jaeger, xray, ottrace, none).
- `sampler.type` goes to `OTEL_TRACES_SAMPLER` and `sampler.argument` to `OTEL_TRACES_SAMPLER_ARG`; the argument depends on the sampler (for `parentbased_traceidratio` a number from 0 to 1).
- `OTEL_NODE_IP` and `OTEL_POD_IP` are injected automatically so an endpoint can reference them.

Python, DotNet and Go auto-instrumentation use http/proto by default, so if `exporter.endpoint` uses port 4317 (gRPC) you must override `OTEL_EXPORTER_OTLP_ENDPOINT` in that language's `env` to port 4318. An `https://` endpoint requires `exporter.tls`.

Env var precedence from the API reference: original container env vars, then language-specific env, then common `spec.env`, then values derived from the spec.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/README.md: the supported language list, `kubectl get otelinst`, propagators added to `OTEL_PROPAGATORS`, automatic `OTEL_NODE_IP` and `OTEL_POD_IP`, and the http/proto default with port 4318 for Python, DotNet and Go. Confirmed against the Instrumentation API reference (docs/api/instrumentations.md, read as raw Markdown): the propagators enum (tracecontext, baggage, b3, b3multi, jaeger, xray, ottrace, none), `sampler.type` to `OTEL_TRACES_SAMPLER` with its enum, `sampler.argument` to `OTEL_TRACES_SAMPLER_ARG` (0 to 1 for parentbased_traceidratio), the https endpoint requiring `exporter.tls`, and the env var precedence order (original container variables, language specific, common, then instrument spec). Nothing removed.

Method: documentation only; no commands were run.
