---
id: computing-software.cloud-infrastructure-engineering.observability.otel-sdk-environment-variables
name: otel-sdk-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [otel-exporter-otlp-env, otel-resource-attributes-env, language-instrumentation, otlp, sdk-configuration]
level: practitioner
status: docs-checked
description: "Configure any OpenTelemetry SDK with OTEL_* env vars: OTLP endpoint/protocol/headers per signal, resource attributes, exporters, samplers, intervals, and URL/encoding traps."
sources: ["https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/", "https://opentelemetry.io/docs/specs/otel/protocol/exporter/", "https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTEL_* environment configuration

## OTLP exporter
| Var | Notes |
|---|---|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | base URL; gRPC `http://host:4317`, HTTP `http://host:4318` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc`, `http/protobuf` (spec default), `http/json` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` (and `_METRICS_`, `_LOGS_`) | **full URL** incl. `/v1/traces` for HTTP |
| `OTEL_EXPORTER_OTLP_HEADERS` | `key1=value1,key2=value2` (W3C Baggage header format, no semicolon metadata; values are strings) |
| `OTEL_EXPORTER_OTLP_COMPRESSION` | `gzip` (the only value the spec lists; no default in the spec) |
| `OTEL_EXPORTER_OTLP_TIMEOUT` | milliseconds, default 10s; overall time per batch export including retries |
| `OTEL_EXPORTER_OTLP_CERTIFICATE`, `_CLIENT_CERTIFICATE`, `_CLIENT_KEY` | TLS / mTLS |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | `cumulative` (default), `delta`, `lowmemory` (case-insensitive) |

**Trap**: for OTLP/HTTP the generic `OTEL_EXPORTER_OTLP_ENDPOINT` is a base URL and the SDK appends `v1/traces`, `v1/metrics`
or `v1/logs`; a per-signal endpoint is used as-is (only an empty path becomes `/`). So
`OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://c:4318` posts to the root path, not `/v1/traces`. SDK default endpoints are
`http://localhost:4318` (HTTP) and `http://localhost:4317` (gRPC).

## Resource and service
`OTEL_SERVICE_NAME=checkout` (wins over `service.name` in attributes);
`OTEL_RESOURCE_ATTRIBUTES=service.namespace=shop,deployment.environment.name=prod` (comma-separated `key=value`; the spec
requires percent-encoding for characters outside the allowed set, so use `%20` for spaces).

## Exporters and SDK
`OTEL_TRACES_EXPORTER` (`otlp` default, `zipkin`, `console`, `none`), `OTEL_METRICS_EXPORTER` (`otlp` default, `prometheus`,
`console`, `none`), `OTEL_LOGS_EXPORTER` (`otlp` default, `console`, `none`); `logging` is a deprecated alias for console. The
spec lets an implementation accept a comma-separated list. `OTEL_SDK_DISABLED=true` disables the SDK for all signals (default
false), `OTEL_PROPAGATORS` (default `tracecontext,baggage`), `OTEL_TRACES_SAMPLER` (default `parentbased_always_on`) with
`OTEL_TRACES_SAMPLER_ARG` (for `traceidratio` and `parentbased_traceidratio` a probability in [0..1], default 1.0),
`OTEL_METRIC_EXPORT_INTERVAL` (default 60000 ms), `OTEL_BSP_*` (span processor: schedule delay 5000 ms, queue 2048, batch 512)
and `OTEL_BLRP_*` (log record processor: schedule delay 1000 ms, queue 2048, batch 512), `OTEL_LOG_LEVEL` (default `info`,
SDK internal logger).
Prometheus exporter: `OTEL_EXPORTER_PROMETHEUS_HOST` (default `localhost`) and `OTEL_EXPORTER_PROMETHEUS_PORT` (default 9464).

## Kubernetes pattern
```yaml
env:
  - {name: OTEL_SERVICE_NAME, valueFrom: {fieldRef: {fieldPath: "metadata.labels['app.kubernetes.io/name']"}}}
  - {name: NODE_IP, valueFrom: {fieldRef: {fieldPath: status.hostIP}}}
  - {name: POD_NAME, valueFrom: {fieldRef: {fieldPath: metadata.name}}}
  - {name: OTEL_EXPORTER_OTLP_ENDPOINT, value: "http://$(NODE_IP):4318"}
  - {name: OTEL_RESOURCE_ATTRIBUTES, value: "k8s.pod.name=$(POD_NAME),deployment.environment.name=prod"}
```
`$(VAR)` expansion only works for variables defined earlier in the `env` list (Kubernetes docs); the Downward API supports
`metadata.labels['<KEY>']` and `status.hostIP` field paths.

## Gotchas
- Match protocol and port: 4317 is conventionally gRPC and 4318 HTTP, so set `OTEL_EXPORTER_OTLP_PROTOCOL` explicitly.
- If `OTEL_SERVICE_NAME` and `service.name` in `OTEL_RESOURCE_ATTRIBUTES` are both set, `OTEL_SERVICE_NAME` wins.
- If `OTEL_CONFIG_FILE` is set, the configuration file takes precedence over all other SDK environment variables.
- Not every SDK supports every variable; check the language's SDK documentation.

## Checked

2026-10-24. OpenTelemetry specification (main branch): configuration/sdk-environment-variables.md, protocol/exporter.md, metrics/sdk_exporters/otlp.md, resource/sdk.md; Kubernetes website docs on interdependent environment variables and the Downward API. Confirmed: OTLP exporter variable names, protocol options and default, endpoint construction rules and defaults, headers format, timeout default, compression value, temporality preference values and default, service name precedence, exporter selection values and defaults, batch processor defaults, Prometheus exporter defaults, and `OTEL_CONFIG_FILE` precedence.

Method: documentation only; no commands were run.
