---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-env-vars-and-set-overrides
name: jaeger-env-vars-and-set-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, config-env-var, set-flag, jaeger-listen-host, otel-exporter-otlp-endpoint]
level: practitioner
status: docs-checked
description: "Use ${env:VAR:-default} in the YAML and the --set flag to override values, since Jaeger v2 does not read v1-style environment variables."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
  - https://www.jaegertracing.io/docs/2.22/operations/monitoring/
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: parameterize a Jaeger v2 config.

Jaeger v2 can only be configured via a config file; it does not recognize environment variables the way Jaeger v1 did. The YAML format can, however, refer to environment variables. In this snippet the host is localhost by default, and overridden by `JAEGER_LISTEN_HOST` (useful in a container, where it needs to be 0.0.0.0):
```
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: "${env:JAEGER_LISTEN_HOST:-localhost}:4317"
      http:
        endpoint: "${env:JAEGER_LISTEN_HOST:-localhost}:4318"
```
Environment variables that Jaeger v2 does recognize automatically are those that control the OpenTelemetry Go SDK, such as `OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318`.

Command-line overrides: pass `--set` flags, for example
`--set=receivers.otlp.protocols.grpc.endpoint=0.0.0.0:4317`
This is handy for the all-in-one role, which relies on a built-in config.

Self-tracing can be disabled with the environment variable `OTEL_TRACES_SAMPLER=always_off`.

Failure mode: binding to localhost inside a container makes the port unreachable from outside; the troubleshooting guide recommends listening on 0.0.0.0 for containers.

## Checked

2026-11-03. Confirmed against the Configuration page: Jaeger v2 is configured only by file, the ${env:JAEGER_LISTEN_HOST:-localhost} example, OTel SDK variables such as OTEL_EXPORTER_OTLP_ENDPOINT, and the --set example for the all-in-one role; OTEL_TRACES_SAMPLER=always_off is from the Monitoring page and the 0.0.0.0 advice from the Troubleshooting page. Removed: a closing paragraph with unverified advice on when to use each mechanism.
Method: documentation only; no commands were run.
