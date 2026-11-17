---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-metrics-backends-prometheus-otlp-stackdriver
name: opa-gatekeeper-metrics-backends-prometheus-otlp-stackdriver
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, metrics-backend, prometheus, opentelemetry, otlp, stackdriver, port-8888]
level: practitioner
status: docs-checked
description: "Export Gatekeeper metrics to Prometheus (port 8888), an OpenTelemetry collector or Stackdriver using --metrics-backend and related flags."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper metrics backends prometheus otlp stackdriver

`--metrics-backend` selects exporters and can be repeated. Omitting it supports Prometheus only.

- Prometheus (default): metrics at port `8888`, path `/metrics`; point a Prometheus scrape job at it. Change the port with `--prometheus-port`.
- OpenTelemetry: `--otlp-endpoint` sets the collector endpoint (HTTP exporter only) and `--otlp-metric-interval` the read interval (10 seconds if unspecified). Use it to reach any backend the collector supports.
- Stackdriver (Google Cloud operations suite): `--stackdriver-only-when-available` starts the exporter only if credentials are available; `--stackdriver-metric-interval` sets the interval (10 seconds if unspecified).

Example container args for dual export: `--metrics-backend=prometheus --metrics-backend=opentelemetry --otlp-endpoint=<collector host and port>`.

For counters, Prometheus client libraries recommend the `_total` suffix and often append it automatically, so check the exact series name in your Prometheus before writing alert rules for `gatekeeper_validation_request_count`.

## Checked

2026-11-04. Confirmed against metrics.md (Metric Backends). Removed or corrected: a closing paragraph that repeated the flag list and gave generic advice.

Method: documentation only; no commands were run.
