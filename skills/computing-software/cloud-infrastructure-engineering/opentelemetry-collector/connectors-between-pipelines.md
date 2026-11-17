---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.connectors-between-pipelines
name: connectors-between-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, connector, pipeline, count, forward, routing]
level: advanced
status: docs-checked
description: "Join two pipelines with a connector, which acts as an exporter in one pipeline and a receiver in the next."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Connectors join two pipelines, acting as both exporter and receiver. A connector consumes data as an exporter at the end of one pipeline and emits data as a receiver at the beginning of another. The data consumed and emitted may be of the same type or different types, and you can use connectors to summarize, replicate or route data. By default no connectors are configured, and configuring one does not enable it; it must be used in pipelines in the `service` section.

The page's example uses the `count` connector to produce a metric `my.prod.event.count` from span events whose `env` attribute is `prod` or whose name is `prodevent`. The conditions are ORed and select events to count rather than filtering traces:

```yaml
connectors:
  count:
    spanevents:
      my.prod.event.count:
        description: The number of span events matching either condition.
        conditions:
          - 'attributes["env"] == "prod"'
          - 'name == "prodevent"'
service:
  pipelines:
    traces:
      receivers: [foo]
      exporters: [count]
    metrics:
      receivers: [count]
      exporters: [bar]
```

Points from the page:

- A processor cannot export traces from a pipeline as metrics in another pipeline, but a connector can.
- This example does not export the original traces to a backend; add a trace exporter to the traces pipeline's `exporters` list to keep them.
- Each connector type works with specific pairs of data types and may only connect pipelines accordingly.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
