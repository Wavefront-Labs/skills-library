---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-command-line-flags
name: telegraf-command-line-flags
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [commands, cli, flags, telegraf-command, usage]
level: practitioner
status: docs-checked
description: "Summarises the telegraf command, its subcommands and the main global flag groups for loading config, run modes, plugin selection and debugging."
sources: ["https://docs.influxdata.com/telegraf/v1/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The telegraf command and global flags

Usage: `telegraf [commands]` or `telegraf [flags]`.

## Commands

`config` (generate or migrate configs), `plugins` (print available plugins), `secrets`, `service` (Windows only), `version`.

## Flag groups

- **Load configuration**: `--config` (path or URL, repeatable), `--config-directory`, `--config-url-retry-attempts`, `--config-url-watch-interval`, `--watch-config`, `--watch-interval`, `--watch-debounce-interval`.
- **Run modes**: `--test`, `--test-wait <seconds>`, `--once`.
- **Select plugins**: `--input-filter`, `--output-filter`, `--processor-filter`, `--aggregator-filter`, `--secretstore-filter`, `--section-filter` (all colon-separated), and `--select` for label selectors.
- **Print information**: `--usage <plugin>`, `--input-list`, `--output-list`, `--deprecation-list`, `--print-plugin-config-source`, `--help`.
- **Secrets and environment**: `--password`, `--unprotected`, `--strict-env-handling`, `--non-strict-env-handling`, `--old-env-behavior`.
- **Logging and debugging**: `--debug`, `--quiet`, `--pprof-addr`, `--pidfile`.

The old `--version` flag is deprecated; use `telegraf version`.

Global flags go before the subcommand: `telegraf --config my.conf secrets list`.

## Plugin listing

`telegraf plugins` has subcommands inputs, outputs, processors, aggregators and secretstores; `--deprecated` prints only deprecated ones.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Telegraf commands page: command list and every flag group, deprecated --version. Removed: nothing.

Method: documentation only; no commands were run.
