---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-generating-configuration
name: telegraf-generating-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [config-generation, input-filter, output-filter, section-filter, powershell-encoding]
level: practitioner
status: docs-checked
description: "Shows how to generate a Telegraf configuration with telegraf config, restrict it by plugin and section filters, and avoid the PowerShell 5 encoding trap."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/file/", "https://docs.influxdata.com/telegraf/v1/commands/config/", "https://docs.influxdata.com/telegraf/v1/commands/config/create/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generating a configuration

`telegraf config` (the default `create` subcommand) prints a configuration including all available plugins with documented defaults:

```sh
telegraf config > telegraf.conf
```

## Limiting what is generated

Filters take colon-separated names:

```sh
telegraf config --input-filter cpu:mem:net:swap --output-filter influxdb_v3:kafka
```

Available filters: `--section-filter` (valid values `agent`, `global_tags`, `outputs`, `processors`, `aggregators`, `inputs`), `--input-filter`, `--output-filter`, `--aggregator-filter`, `--processor-filter`, `--secretstore-filter`. For example, only a Modbus input and an InfluxDB v2 output:

```sh
telegraf config --section-filter "inputs:outputs" --input-filter "modbus" --output-filter "influxdb_v2"
```

## Windows PowerShell 5

PowerShell 5 writes UTF-16LE by default but Telegraf expects UTF-8. Set the encoding:

```powershell
telegraf.exe config | Out-File -Encoding utf8 telegraf.conf
```

PowerShell 6 and later, Command Prompt and Git Bash produce UTF-8 by default.

## Plugin help

`telegraf --usage <plugin>` prints a plugin's sample configuration, for example `telegraf --usage mysql`.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): config create, Configuration file page (filters, section values, PowerShell 5 encoding), commands page for --usage. Removed: nothing.

Method: documentation only; no commands were run.
