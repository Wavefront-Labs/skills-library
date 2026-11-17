---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-config-yaml-format
name: jaeger-config-yaml-format
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, config-yaml, otel-collector-format, receivers-processors-exporters, jaeger-config]
level: practitioner
status: docs-checked
description: "Configure Jaeger v2 with one YAML file in OpenTelemetry Collector format and find the working example configs."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand how Jaeger v2 is configured.

Jaeger v2 uses a YAML file in the same format as the OpenTelemetry Collector. It defines the ingestion pipeline as receivers, processors, connectors and exporters, plus Jaeger-specific extensions that provide the unique capabilities (storage, query, remote sampling).

Run it with:
`jaeger --config config.yaml`

Working examples live in the Jaeger repository:
- `config-{storage}.yaml`: collector role with a given storage backend
- `config-query.yaml`: standalone query role with the UI
- `cmd/jaeger/internal/all-in-one.yaml`: the config bundled into the binary for the all-in-one role
- other examples for SPM, tail sampling, adaptive sampling and more

The configuration reference is still being expanded; the docs say documentation of all properties will be auto-generated in future, and for the jaeger_query extension they name config.go in the repository as the authoritative source.

Failure mode: Jaeger v2 can only be configured via the config file and does not recognise Jaeger v1 environment variables. The file can reference environment variables, for example `${env:JAEGER_LISTEN_HOST:-localhost}:4317`, and the OpenTelemetry Go SDK variables such as OTEL_EXPORTER_OTLP_ENDPOINT are recognised automatically. `--set=receivers.otlp.protocols.grpc.endpoint=0.0.0.0:4317` overrides single values.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Configuration page, read in full. Removed the role-choice paragraph and the container mount failure mode, which that page does not state.

Method: documentation only; no commands were run.
