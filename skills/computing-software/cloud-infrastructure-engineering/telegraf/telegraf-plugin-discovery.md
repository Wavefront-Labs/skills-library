---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-plugin-discovery
name: telegraf-plugin-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [plugins, plugin-list, usage, deprecation, secretstore-plugins]
level: intro
status: docs-checked
description: "Shows how to discover Telegraf plugins, print a plugin sample configuration and list deprecated plugins from the command line."
sources: ["https://docs.influxdata.com/telegraf/v1/commands/plugins/", "https://docs.influxdata.com/telegraf/v1/commands/", "https://docs.influxdata.com/telegraf/v1/configuration/secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Discovering plugins from the CLI

## Listing

`telegraf plugins` prints available plugins. Subcommands: `inputs`, `outputs`, `processors`, `aggregators`, `secretstores`. Add `--deprecated` to print only deprecated ones.

```sh
telegraf plugins inputs
telegraf plugins --deprecated
```

Global flags `--input-list` and `--output-list` print inputs and outputs too, and `--deprecation-list` prints deprecated plugins and options.

## Sample configuration

`telegraf --usage <plugin>` prints a plugin's usage and sample config, for example `telegraf --usage mysql`. `--print-plugin-config-source` prints the source for a plugin.

## Per-plugin docs

Secret store plugin docs live in the Telegraf GitHub repository under the secretstores plugin folder.

## Startup log

`Loaded inputs` and `Loaded outputs` lines in the startup log list the plugins a running configuration enabled.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Commands and plugins command pages (subcommands, flags), secrets pages (secretstore plugins on GitHub), troubleshoot page (Loaded inputs / outputs lines). Removed: the unsourced plugin-directory remark, the word legacy for the list flags, and the debug = true condition on the startup lines.

Method: documentation only; no commands were run.
