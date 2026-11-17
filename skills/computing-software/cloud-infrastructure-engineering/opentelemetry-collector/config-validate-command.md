---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.config-validate-command
name: config-validate-command
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, configuration, validate, ci, otelcol]
level: intro
status: docs-checked
description: "Check a Collector configuration file with the otelcol validate command."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To validate a configuration file, use the `validate` command.

```
otelcol validate --config=file:/path/to/otelcol.yaml
```

List the components a distribution contains with `otelcol components`.

Configuring a component does not enable it: receivers, processors, exporters and connectors are enabled by listing them in `service::pipelines`, and extensions in `service::extensions`. Read the `service` section yourself to confirm the data path you intended.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
