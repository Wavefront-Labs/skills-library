---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-configuration-file-structure
name: telegraf-configuration-file-structure
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [configuration, toml, global-tags, agent, plugin-tables]
level: intro
status: docs-checked
description: "Describes the three parts of a Telegraf configuration file and the minimum valid configuration. Use when writing or reviewing a telegraf.conf."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/file/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configuration file structure

The configuration file is TOML with three sections:

- `[global_tags]`: tags applied to all gathered metrics.
- `[agent]`: settings controlling how Telegraf itself runs.
- Plugin tables, one per enabled instance, such as `[[inputs.cpu]]` or `[[outputs.influxdb_v3]]`.

```toml
[global_tags]
  dc = "us-east-1"

[agent]
  interval = "10s"
  flush_interval = "10s"

[[inputs.cpu]]
  percpu = true

[[outputs.influxdb_v3]]
  urls = ["http://localhost:8181"]
  database = "your_database"
```

## Validity

A configuration must enable at least one input and at least one output. If either is missing, Telegraf exits at startup with an invalid-configuration error. The exception is `telegraf --test`, which prints gathered metrics and needs no output.

## Locations

Use `--config` for a path or URL, and `--config-directory` to load every `.conf` file in a directory. The defaults on most systems are `/etc/telegraf/telegraf.conf` and `/etc/telegraf/telegraf.d`. On Windows they are `telegraf.conf` and `telegraf.d` in the installation directory.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 source for the Telegraf configuration file page (first 150 lines read: structure, validity, generation and locations).
