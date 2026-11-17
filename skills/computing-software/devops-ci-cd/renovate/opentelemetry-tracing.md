---
id: computing-software.devops-ci-cd.renovate.opentelemetry-tracing
name: opentelemetry-tracing
category: computing-software
field: devops-ci-cd
product: renovate
tags: [opentelemetry, tracing, otlp, renovate]
level: advanced
status: docs-checked
description: "Trace Renovate runs with OpenTelemetry by setting OTEL_EXPORTER_OTLP_ENDPOINT and understanding what is supported."
sources:
  - https://docs.renovatebot.com/opentelemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate supports the OpenTelemetry standard, but the feature is flagged experimental: attribute names may change even in non-major releases, although it is considered stable enough for production.

The OpenTelemetry Protocol carries traces, metrics and logs. Renovate supports only traces and some metrics. It does not emit stats on caching, error events or number of found updates.

Activate it by setting the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable. Once set, you can use the other variables from the OpenTelemetry SDK environment specification.

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector.example.com:4318 \
OTEL_SERVICE_NAME=renovate renovate my-org/my-repo
```

What the trace shows:

- A run against a repository is split into traced "splits": `init`, `extract`, `lookup` and `update`. A viewer like Jaeger displays them as a timeline, with HTTP calls, git operations, `rawExec:` command executions, per-manager traces under `extract` and `lookup`, and per-branch traces under `update`. Cache load/save operations are traced too.
- Metrics and logs in OTLP format are not supported; the docs suggest the collector's spanmetrics connector to derive metrics from traces.

Other environment variables: `OTEL_SERVICE_NAME` (default `renovate`), `OTEL_SERVICE_NAMESPACE` (default `renovatebot.com`), `OTEL_SERVICE_VERSION` (default the Renovate release version). Choose the exporter protocol with `OTEL_EXPORTER_OTLP_PROTOCOL` (or `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`, which takes precedence): `grpc`, `http/protobuf` or `http/json`; with neither set, Renovate uses `http/json`.

Cloud resource detectors (AWS, GCP, Azure, GitHub, env) are on by default; set `RENOVATE_USE_CLOUD_METADATA_SERVICES=false` to leave only the env detector, or pick detectors with `OTEL_NODE_RESOURCE_DETECTORS` (`all` default, `none`, or a comma list of `aws`, `azure`, `gcp`, `github`, `env`).

Debugging: `RENOVATE_TRACING_CONSOLE_EXPORTER` prints telemetry to the console, `OTEL_LOG_LEVEL` sets the SDK diagnostics level, and `RENOVATE_TRACING_FILE_EXPORTER_PATH` writes OTLP JSON NDJSON to a file. An example local Docker setup is on the OpenTelemetry examples page of the docs (not read here).

## Checked

2026-11-08: read the whole OpenTelemetry page (raw source of docs.renovatebot.com/opentelemetry). Confirmed the experimental warning, traces-only support, `OTEL_EXPORTER_OTLP_ENDPOINT`, the service name, namespace and version variables and defaults, the three protocols and the `http/json` default, resource detectors and their switches, the traced splits, the file and console exporters and `OTEL_LOG_LEVEL`. The linked OpenTelemetry examples page was not read. Removed the unsourced advice about internal collectors and sampling, and the claim that only `init` and `extract` appear.
Method: documentation only; no commands were run.
