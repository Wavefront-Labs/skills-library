---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-hot-reload-config
name: telegraf-hot-reload-config
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [watch-config, reload, sighup, config-reload, notify]
level: advanced
status: docs-checked
description: "Compares the ways to reload Telegraf configuration without a full restart: SIGHUP via systemctl reload, --watch-config and the remote URL watch interval."
sources: ["https://docs.influxdata.com/telegraf/v1/configuration/file/", "https://docs.influxdata.com/telegraf/v1/administer/run-as-service/", "https://docs.influxdata.com/telegraf/v1/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reloading configuration

Telegraf offers several routes.

## SIGHUP

On systemd, `sudo systemctl reload telegraf` sends `SIGHUP`; Telegraf reloads its configuration files without restarting the process.

## --watch-config

Start Telegraf with `--watch-config <method>` to react to local file changes. The command reference describes `notify` (filesystem notifications on Linux, BSD and macOS) and polling. Related flags:

- `--watch-interval <duration>`: polling period, used with the poll method; disabled by default.
- `--watch-debounce-interval <duration>`: wait after a change before reloading.

The flag documentation describes it as restarting Telegraf on local configuration changes.

## Remote configurations

`--config-url-watch-interval` checks the URL at the given interval with an HTTP HEAD request and compares `Last-Modified`. A changed value triggers a reload. A failed check logs a warning and keeps the current configuration. It is disabled by default.

Each configuration file must be valid TOML on its own.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Configuration file page (--watch-config, URL watch with HEAD and Last-Modified, warning on failed check), run-as-service (SIGHUP reload), commands page flags. Removed: the unsourced advice to run a --test pass before reloading.

Method: documentation only; no commands were run.
