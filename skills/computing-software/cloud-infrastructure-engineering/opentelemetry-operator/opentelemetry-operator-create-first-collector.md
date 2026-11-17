---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-create-first-collector
name: opentelemetry-operator-create-first-collector
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, opentelemetrycollector, first-collector, otlp-receiver, memory-limiter, config-validation]
level: intro
status: docs-checked
description: "Create a minimal OpenTelemetryCollector resource with an OTLP receiver, memory_limiter and debug exporter, and know that the operator does not validate the full config."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/collector.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Create your first OpenTelemetryCollector

Once the operator deployment is ready, create a Collector instance with an `OpenTelemetryCollector` resource. The documented minimal example uses apiVersion `opentelemetry.io/v1beta1`:

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: simplest
spec:
  config:
    receivers:
      otlp:
        protocols:
          grpc: {endpoint: 0.0.0.0:4317}
          http: {endpoint: 0.0.0.0:4318}
    processors:
      memory_limiter:
        check_interval: 1s
        limit_percentage: 75
        spike_limit_percentage: 15
    exporters:
      debug: {}
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter]
          exporters: [debug]
```

The `config` node holds the YAML passed through as-is to the underlying Collector, so use the upstream Collector documentation for the available components. The `debug` exporter writes spans to the stdout of the Collector pod.

Caveats stated in the docs:
- The operator does not validate the whole configuration. An invalid config can still create the instance while the Collector container crashes, so check pod logs.
- Until the Collector config format is stable, an example may need changes to match the Collector image version being used.
- Empty maps such as `debug` must be written as `{}` in v1beta1.

## Checked

2026-11-04. Confirmed against docs/getting-started/collector.md: the v1beta1 example (OTLP receiver on 4317 and 4318, `memory_limiter` with 1s, 75 and 15, `debug` exporter, traces pipeline), the `config` passed as-is to the Collector, the debug exporter writing to the Collector's stdout, the warning that the config format may change, and the note that the operator does not validate the whole configuration. Confirmed against docs/reference/crd-changelog.md: empty maps need an explicit `{}` in v1beta1. The skill's flow-style `grpc: {endpoint: ...}` is an equivalent rewrite of the page's block form. Nothing removed.

Method: documentation only; no commands were run.
