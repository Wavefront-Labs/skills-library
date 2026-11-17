---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.config-component-ids-and-sections
name: config-component-ids-and-sections
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, configuration, receivers, processors, exporters, service]
level: intro
status: docs-checked
description: "Understand the Collector configuration layout: component sections, type/name identifiers and the service section that wires them."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Collector configuration has four pipeline component classes (receivers, processors, exporters, connectors) plus extensions, and a `service` section that decides which are enabled. Configuring a component does not enable it: receivers, processors, exporters and connectors are enabled by listing them in `service::pipelines`, and extensions in `service::extensions`.

Each component has an identifier of the form `type[/name]`, for example `otlp` or `otlp/2`. You can define a type more than once as long as identifiers are unique. Pipelines use the same syntax, such as `traces/2`:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
  otlp/2:
    protocols:
      grpc:
        endpoint: 0.0.0.0:55690
exporters:
  otlp_grpc:
    endpoint: otelcol:4317
  otlp_grpc/2:
    endpoint: otelcol2:4317
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [otlp_grpc]
    traces/2:
      receivers: [otlp/2]
      exporters: [otlp_grpc/2]
```

Further points from the page:

- Pipeline types are `traces`, `metrics` and `logs`.
- Processor order in a pipeline is the processing order.
- A processor used in several pipelines gets a separate instance in each.
- The Collector requires at least one receiver and one exporter.
- `service::telemetry` has `logs` and `metrics` subsections for the Collector's own observability.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
