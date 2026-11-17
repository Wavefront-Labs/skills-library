---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.config-multiple-files-and-set
name: config-multiple-files-and-set
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, configuration, merge, set-flag, override]
level: practitioner
status: docs-checked
description: "Merge several Collector configuration sources and override single values with repeated --config and --set flags."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can pass several configurations with repeated `--config` flags. Each file can be a full or partial configuration, and files can reference components from each other. The Collector merges them into one in-memory configuration. If the merged result is not complete, you get an error, because required components are not added by default.

```shell
otelcol --config=file:/path/to/first/file --config=file:/path/to/second/file
```

`--set` overrides single settings, merged into the final configuration after all `--config` sources are resolved and merged. It takes one key/value pair per flag, and `::` separates nested keys:

```shell
otelcol --set outer::inner=value
```

which is the YAML `outer: { inner: value }`.

Further points from the page:

- Use `::` rather than dots in YAML paths to avoid confusion with names that contain dots, for example `receivers::docker_stats::metrics::container.cpu.utilization::enabled: false`.
- Validate with `otelcol validate --config=customconfig.yaml`.
- Inspect the final result with `otelcol print-config --config=...` together with `--feature-gates=otelcol.printInitialConfig`. It is experimental, redacts sensitive fields by default, and `--mode=unredacted` shows them. `--validate=false` prints an invalid configuration, and `--format=json` is unstable.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
