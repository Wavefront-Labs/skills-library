---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.internal-telemetry-traces-views
name: internal-telemetry-traces-views
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, internal-telemetry, traces, views, metrics, otlp]
level: sme
status: docs-checked
description: "Export the Collector's own traces and reshape internal metrics with service::telemetry views."
sources:
  - https://opentelemetry.io/docs/collector/internal-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Collector does not expose traces about itself by default, but it can be configured to. The page calls internal tracing experimental, with no guarantee about the stability of span names and attributes.

```yaml
service:
  telemetry:
    traces:
      processors:
        - batch:
            exporter:
              otlp:
                protocol: http/protobuf
                endpoint: https://backend:4318
```

Metric views reshape internal metrics. This example emits `otelcol_process_uptime` under a new name and description:

```yaml
service:
  telemetry:
    metrics:
      views:
        - selector:
            instrument_name: otelcol_process_uptime
            instrument_type:
          stream:
            name: process_uptime
            description: The amount of time the Collector has been up
```

Further points from the page:

- Always use the OTLP name in `instrument_name`, such as `otelcol_process_uptime`, whatever Prometheus suffixes are configured.
- Views can also change the aggregation, attributes and cardinality limits; the page points to the OpenTelemetry Configuration schema's view examples.
- OTLP exporter options include `endpoint`, `protocol` (required: `grpc` or `http/protobuf`), `compression`, `timeout` (default 10000 ms), `headers`, `certificate`, `client_certificate` and `client_key`.
- Prefer the Collector's YAML over environment-variable SDK configuration, which it overrides.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/internal-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
