---
id: computing-software.networking-hardware-and-wireless.traefik.metrics-prometheus-and-otlp
name: metrics-prometheus-and-otlp
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, metrics, prometheus, otlp, datadog, statsd, influxdb]
level: practitioner
status: docs-checked
description: "Export Traefik metrics with Prometheus or OTLP and control label cardinality for entrypoints, routers and services."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/observability/metrics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# metrics prometheus and otlp
Supported metric backends: OpenTelemetry/OTLP (HTTP to https://localhost:4318 by default), Datadog, InfluxDB2, Prometheus and StatsD. Prometheus options: `addEntryPointsLabels` (default true), `addRoutersLabels` (default false), `addServicesLabels` (default true), `buckets` (default 0.1, 0.3, 1.2, 5.0), `manualRouting`, `entryPoint` (default `traefik`) and `headerLabels` (extra labels taken from request headers for the requests_total metrics).

```yaml
metrics:
  prometheus:
    addRoutersLabels: true
    buckets: [0.1, 0.3, 1.2, 5.0]
    entryPoint: metrics
entryPoints:
  metrics:
    address: ":9100"
```
The Prometheus metrics are exposed on the entrypoint named by `entryPoint` (the example uses a dedicated `metrics` entrypoint on `:9100`).

Gotchas: `addRoutersLabels` is off by default while `addEntryPointsLabels` and `addServicesLabels` are on. `manualRouting: true` disables the default internal router so you can create a custom router for the `prometheus@internal` service. The default `entryPoint` is `traefik`.

## Checked
2026-11-03. Confirmed against the Traefik metrics reference page: supported backends, the OTLP default endpoint, and the Prometheus options and defaults (`addEntryPointsLabels`, `addRoutersLabels`, `addServicesLabels`, `buckets`, `manualRouting`, `entryPoint`, `headerLabels`). Removed: the cardinality and overload claims, the scrape path and metric-name Verify step.
Method: documentation only; no commands were run.


