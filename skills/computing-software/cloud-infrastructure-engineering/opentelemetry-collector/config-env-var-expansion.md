---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.config-env-var-expansion
name: config-env-var-expansion
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, configuration, environment-variables, expansion, secrets]
level: practitioner
status: docs-checked
description: "Use environment variables in Collector configuration with ${env:VAR} and ${env:VAR:-default}, and escape literal dollar signs."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Collector expands environment variables inside configuration values. The page example:

```yaml
processors:
  attributes/example:
    actions:
      - key: ${env:DB_KEY}
        action: ${env:OPERATION}
```

Defaults use the bash syntax `${env:DB_KEY:-some-default-var}`:

```yaml
processors:
  attributes/example:
    actions:
      - key: ${env:DB_KEY:-mydefault}
        action: ${env:OPERATION:-}
```

Use `$$` for a literal `$`. For a value such as `$DataVisualization`:

```yaml
exporters:
  prometheus:
    endpoint: prometheus:8889
    namespace: $$DataVisualization
```

Related points from the same page:

- The same `${...}` mechanism includes files, as in `exporters: ${file:exporters.yaml}`, which merges the file's content in place.
- The `env` scheme can also supply the whole configuration with `--config=env:MY_CONFIG_IN_AN_ENVVAR`.
- Proxy settings come from the `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` environment variables, which exporters using `net/http` respect when set at start time.

The file form works like this. With `exporters: ${file:exporters.yaml}` in the main configuration, and `exporters.yaml` containing `otlp_grpc:` with `endpoint: otelcol.observability.svc.cluster.local:443`, the in-memory result has that block under `exporters`.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
