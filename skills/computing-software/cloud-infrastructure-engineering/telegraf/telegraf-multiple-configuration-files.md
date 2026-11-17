---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-multiple-configuration-files
name: telegraf-multiple-configuration-files
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [config-directory, multiple-files, agent-table, toml]
level: practitioner
status: docs-checked
description: "Explains how Telegraf merges multiple configuration files and the rules for the agent table and plugin definitions. Use when splitting config into telegraf.d fragments."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/file/", "https://docs.influxdata.com/telegraf/v1/configuration/toml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using multiple configuration files

Telegraf parses each loaded file separately and merges all settings as if they were one file. Load extra files with repeated `--config` flags or `--config-directory`, which loads every file ending in `.conf`. The default directory on most systems is `/etc/telegraf/telegraf.d`.

## Rules

- Every file must be valid TOML on its own. Files are not concatenated before parsing, so one plugin definition cannot be split across files.
- Define `[agent]` only once, in the first file Telegraf reads.
- Any plugin can be defined multiple times, across any files.

If a single plugin definition must be assembled from fragments, concatenate them into one valid file with your own tooling before starting Telegraf.

## Reloading

Start Telegraf with `--watch-config` to reload local configuration files when they change. The command reference lists `notify` (filesystem notifications on Linux, BSD and macOS) and `poll` as methods, with `--watch-interval` for polling and `--watch-debounce-interval` to wait after a change before reloading.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Configuration file page: merging rules, default directory, --watch-config; commands page for watch flags. Removed: the unsourced remark that TOML has no concept of multiple files.

Method: documentation only; no commands were run.
