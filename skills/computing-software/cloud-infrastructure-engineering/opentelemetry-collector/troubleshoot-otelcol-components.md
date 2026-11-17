---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.troubleshoot-otelcol-components
name: troubleshoot-otelcol-components
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, troubleshooting, components, distribution, otelcol]
level: intro
status: docs-checked
description: "List the receivers, processors, exporters, connectors and extensions built into your Collector binary with otelcol components."
sources:
  - https://opentelemetry.io/docs/collector/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `otelcol components` sub-command lists the components available in a Collector distribution, including their stability levels. The page notes that the output format might change across versions.

```shell
otelcol components
```

The sample output starts with `buildinfo` (command, description, version), then lists receivers, processors, exporters, connectors and extensions. Each entry has a `name` and a `stability` map per signal, for example:

```yaml
receivers:
  - name: otlp
    stability:
      logs: Beta
      metrics: Stable
      traces: Stable
extensions:
  - name: zpages
    stability:
      extension: Beta
```

Connectors show pairs such as `traces-to-traces` and `metrics-to-metrics`. Values seen in the page's sample include `Undefined`, `Development`, `Alpha`, `Beta` and `Stable`. Use the command to see which components your build contains.

Related checks on the pages:

- A receiver defined but not listed in any pipeline receives nothing, which is a common cause of not receiving data.
- In Kubernetes, ephemeral debug containers can help investigate the Collector.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/troubleshooting page (docs repo raw markdown).
