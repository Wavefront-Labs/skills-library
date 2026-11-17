---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.internal-telemetry-metrics-port-8888
name: internal-telemetry-metrics-port-8888
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, internal-telemetry, metrics, prometheus, port-8888, otelcol]
level: practitioner
status: docs-checked
description: "Scrape the Collector's own metrics from port 8888 and configure readers under service::telemetry::metrics."
sources:
  - https://opentelemetry.io/docs/collector/internal-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the Collector generates basic metrics about itself and exposes them through the OpenTelemetry Go Prometheus exporter, scrapeable at `http://127.0.0.1:8888/metrics`. Logs go to `stderr`.

To expose the endpoint on all interfaces, which the page suggests for containers, set it under `service::telemetry::metrics`:

```yaml
service:
  telemetry:
    metrics:
      readers:
        - pull:
            exporter:
              prometheus:
                host: '0.0.0.0'
                port: 8888
```

As of v0.123.0, the older `service::telemetry::metrics::address` setting is ignored. To push internal metrics to an OTLP backend instead, use a `periodic` reader with an `otlp` exporter (`protocol: http/protobuf`, `endpoint: https://backend:4318`).

Further points from the page:

- `level` is `none`, `basic`, `normal` (default) or `detailed`, set at `service::telemetry::metrics::level`.
- `with_resource_constant_labels` with `included` labels adds labels from `service::telemetry::resource`.
- The Collector attaches `service.name`, `service.version` and a random `service.instance.id` to internal telemetry; set one to `null` to disable it.
- The OTLP metric exporter's `temporality_preference` defaults to `cumulative`.

The page's summary of observable values includes process uptime and CPU time, memory and heap usage, receiver items accepted and refused, processor incoming and outgoing items, exporter items sent, failed to enqueue and failed to send, and queue size and capacity.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/internal-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
