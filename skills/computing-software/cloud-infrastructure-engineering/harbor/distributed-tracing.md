---
id: computing-software.cloud-infrastructure-engineering.harbor.distributed-tracing
name: distributed-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [distributed-tracing, opentelemetry, jaeger, trace-sample-rate, harbor]
level: advanced
status: docs-checked
description: "Enable Harbor tracing in harbor.yml with one exporter (otel or jaeger), set sample rate and attributes, and know which components emit spans."
sources:
  - https://goharbor.io/docs/main/administration/distributed-tracing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor v2.4 and later can export traces using the OpenTelemetry SDK. Enable it in the `trace` block of `harbor.yml`.

Keys:
- `enabled`: default false.
- `sample_rate`: `1` samples 100 percent of trace data, `0.5` samples 50 percent.
- `namespace`: sets the `service.namespace` attribute to tell Harbor services apart.
- `attributes`: a key-value dictionary of custom attributes added to trace data.
- `otel`: `endpoint` (host and port of an OTel-compatible backend, for example `127.0.0.1:4318`), plus `insecure` to skip certificate verification.
- `jaeger`: `endpoint` (for example `http://127.0.0.1:14268/api/traces`, exports to the collector over HTTP) with optional `username` and `password`, or `agent_host` and `agent_port` to export to a Jaeger agent over UDP.

Only one exporter can be active at a time, and you cannot set both or neither once tracing is enabled. Jaeger endpoint mode and agent mode are also mutually exclusive. To reach several backends, export with `otel` to an OpenTelemetry Collector and let it fan out.

Emitting components: `core`, `jobservice` and `registry` (registryctl). Core traces every received HTTP request, outgoing HTTP calls and database transactions, and adds an `X-Request-ID` to each trace to help find logs. Jobservice traces received and sent HTTP requests and the backend jobs it runs.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Distributed Tracing and the YML file page.
Method: documentation only; no commands were run.
