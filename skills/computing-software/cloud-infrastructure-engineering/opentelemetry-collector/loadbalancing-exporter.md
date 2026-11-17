---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.loadbalancing-exporter
name: loadbalancing-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, loadbalancing, exporter, trace-id, tail-sampling, resolver]
level: advanced
status: docs-checked
description: "Route all spans of a trace to the same backend Collector with the loadbalancing exporter using a static or dns resolver."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/loadbalancingexporter/README.md
  - https://opentelemetry.io/docs/collector/scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The load-balancing exporter consistently routes data to backend Collectors, so a Collector layer in front of tail-sampling or span-to-metrics processors sends all data for one key to the same instance.

```yaml
exporters:
  load_balancing:
    routing_key: traceID
    protocol:
      otlp:
        timeout: 1s
    resolver:
      dns:
        hostname: otelcol.observability.svc.cluster.local
```

Details from the README and scaling page:

- `routing_key` options are `service`, `traceID`, `metric`, `resource`, `streamID`, `attributes` and `randomness`. Defaults: `traceID` for traces, `service` for logs and metrics.
- Resolvers are `static` (a `hostnames` list), `dns`, `k8s` and `aws_cloud_map`; configuring more than one raises an error.
- The DNS resolver defaults to `interval` 5s, `timeout` 1s and port 4317.
- The `k8s` resolver updates faster than DNS and needs RBAC to `get`, `list` and `watch` EndpointSlices.
- Retry, timeout and queue settings under `load_balancing` re-route data when endpoints change; those under `otlp` handle one flaky backend and cannot use a persistent queue.
- The static resolver risks data loss if an endpoint stays down.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/loadbalancingexporter/README.md
- https://opentelemetry.io/docs/collector/scaling/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
