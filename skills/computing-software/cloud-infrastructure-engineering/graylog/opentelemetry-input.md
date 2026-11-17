---
id: computing-software.cloud-infrastructure-engineering.graylog.opentelemetry-input
name: opentelemetry-input
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [opentelemetry, otlp, grpc-input, bearer-token, mutual-tls]
level: practitioner
status: docs-checked
description: "Receive OpenTelemetry logs in Graylog over OTLP gRPC and configure the collector exporter for TLS, bearer token or mutual TLS."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/opentelemetry__grpc__input.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# opentelemetry input

Listener input receiving OpenTelemetry logs over gRPC. Install an OpenTelemetry Collector and add an `otlp` exporter pointing at the Graylog input endpoint (the docs example uses port 4317).

Exporter patterns from the docs:
- Insecure, unauthenticated (`tls: insecure: true`): testing only, not for production.
- TLS with bearer token: a `bearertokenauth` extension with scheme `Bearer` and a token, plus `tls: ca_file`.
- TLS, unauthenticated: `tls: ca_file`.
- Mutual TLS: `ca_file`, `cert_file`, `key_file`.

Add the exporter to the `logs` pipeline under `service`. The snippets are fragments, not full collector configs.

Limitations: only logs are ingested (not metrics or traces), and OTLP over HTTP is not supported, only gRPC.

Data is mapped into Graylog's schema so you can search, analyze and alert on telemetry.

## Checked

2026-11-04. Confirmed against the OpenTelemetry (gRPC) input page, including the tls insecure and ca_file snippets. Added the logs-only and gRPC-only limitations.

Method: documentation only; no commands were run.
