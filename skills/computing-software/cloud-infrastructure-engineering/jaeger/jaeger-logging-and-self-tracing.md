---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-logging-and-self-tracing
name: jaeger-logging-and-self-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, log-level, self-tracing, otel-traces-sampler, health-check-13133]
level: intro
status: docs-checked
description: "Set Jaeger log verbosity, use the health port 13133 and disable or inspect Jaeger's own traces."
sources:
  - https://www.jaegertracing.io/docs/2.22/operations/monitoring/
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
  - https://www.jaegertracing.io/docs/2.22/deployment/
  - https://www.jaegertracing.io/docs/2.22/features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: operate Jaeger's logs and self-observability.

Logs go to stderr in plain text by default; for production the docs recommend verbosity of info or warning. The monitoring page defers to the OpenTelemetry Collector documentation for configuring internal telemetry. The troubleshooting guide says Jaeger gives useful debugging information when the log level is debug. The features page says logs are written to stdout using the structured logging library zap.

Self-tracing: Jaeger traces some of its own components, namely requests to the Query service. After starting all-in-one and refreshing the UI a few times, `jaeger` appears in the Services dropdown. Disable with the environment variable `OTEL_TRACES_SAMPLER=always_off`.

Health: the healthcheckv2 extension serves `/status` on port 13133. The deployment page also lists expvar on 27777 for process-level metrics. The docs suggest health checks for the OpenTelemetry Collector pipeline, storage connectivity and receiver endpoint availability, plus backend health per the storage system's own documentation and network connectivity between components.

Debugging a troubled instance: debug images include delve and listen on TCP 12345 for remote IDE attach.

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 monitoring, troubleshooting, deployment and features pages (read in full); the unconfirmed log-level YAML snippet was removed.
