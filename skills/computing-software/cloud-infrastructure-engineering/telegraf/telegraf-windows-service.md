---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-windows-service
name: telegraf-windows-service
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [windows, service, service-install, auto-restart, error-1067]
level: practitioner
status: docs-checked
description: "Explains running Telegraf as a Windows service: service subcommands, absolute config paths, multiple instances, auto-restart, event log and shutdown timeout."
sources: ["https://docs.influxdata.com/telegraf/v1/administer/run-as-service/", "https://docs.influxdata.com/telegraf/v1/commands/service/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telegraf as a Windows service

The `service` command exists only in Windows builds. On Linux and macOS use systemd or launchd.

## Subcommands

`telegraf.exe service install | uninstall | start | stop | status`. Select a named service with the global `--service-name <name>` (default `telegraf`), placed before `service`.

## Install

Global flags such as `--config` and `--config-directory` are recorded in the service definition, and must use absolute paths. A relative config path makes the service fail at startup with Windows error 1067; reinstall with the absolute path.

```powershell
.\telegraf.exe --config "<absolute path>\telegraf.conf" service install
```

`install` flags: `--display-name` (default `Telegraf Data Collector Service`), `--auto-restart`, `--restart-delay` (default `5m`).

## Restart on failure

The service does not restart on failure by default. Install with `--auto-restart`, optionally `--restart-delay 3m`.

## Multiple services

Seldom needed, since plugins can be defined many times and metrics routed with filtering. If required, install each under a unique `--service-name`.

## Logs and shutdown

Startup messages go to the Windows event log (Application); runtime messages go to the configured log target. On shutdown Telegraf stops plugins and flushes, but Windows kills services after a timeout, usually 5 seconds. Raise the `WaitToKillServiceTimeout` registry value (milliseconds).

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): telegraf service command page and Run Telegraf as a service (Windows section): subcommands, flags, defaults, error 1067, WaitToKillServiceTimeout. Removed: the unconfirmed remark that the registry timeout affects all services.

Method: documentation only; no commands were run.
