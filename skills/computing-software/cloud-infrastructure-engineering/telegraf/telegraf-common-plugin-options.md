---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-common-plugin-options
name: telegraf-common-plugin-options
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [plugin-options, alias, name-override, name-prefix, log-level, interval]
level: practitioner
status: docs-checked
description: "Lists options available to all Telegraf plugins by type: alias, log_level, renaming, tags, per-input timing and per-output flush options. Use when tuning a single plugin instance."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/plugin-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Common plugin options

Any plugin can be defined multiple times; each instance runs independently, so one process can run `inputs.cpu` with different settings.

## All plugins

- `alias`: names an instance for log messages and per-instance stats.
- `log_level`: override of `error`, `warn`, `info`, `debug`, or `trace` (inputs only).

## Inputs, outputs, aggregators: naming

`name_override` replaces the measurement name, `name_prefix` and `name_suffix` add to it. `tags` (inputs and aggregators) adds tags.

```toml
[[inputs.cpu]]
  name_suffix = "_total"
  tags = {tag1 = "foo", tag2 = "bar"}
```

## Inputs

`interval` (default: agent interval), `precision`, `time_source` (`metric` default, `collection_start`, `collection_end`; not for service inputs), `collection_jitter` and `collection_offset` (both must be non-zero to take effect).

## Outputs

`flush_interval`, `flush_jitter`, `metric_batch_size`, `metric_buffer_limit`, each defaulting to the agent value.

```toml
[[outputs.file]]
  files = ["stdout"]
  flush_interval = "1s"
  metric_batch_size = 10
```

Processor `order` and aggregator `period`, `delay`, `grace`, `drop_original` are covered in their own skills.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Plugin options page: all-plugin, naming, input and output options and defaults. Removed: nothing.

Method: documentation only; no commands were run.
