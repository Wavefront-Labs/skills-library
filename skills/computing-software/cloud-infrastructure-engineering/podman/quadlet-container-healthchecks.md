---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-healthchecks
name: quadlet-container-healthchecks
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, healthcheck, healthcmd, healthonfailure, notify-healthy, startup-healthcheck, health-log]
level: advanced
status: docs-checked
description: "Configure Quadlet container healthchecks: HealthCmd, interval, retries, startup checks, log destination and size, HealthOnFailure=kill with systemd, and Notify=healthy."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: have systemd restart unhealthy containers.

Keys equal the matching `podman run --health-*` options: `HealthCmd` (a value of `none` disables existing checks), `HealthInterval` (`disable` results in no automatic timer), `HealthTimeout`, `HealthRetries`, `HealthStartPeriod`.

`HealthOnFailure=` sets the action when the container becomes unhealthy. The page says `kill` integrates best with systemd: the unhealthy container gets killed and systemd restarts the service.

Startup checks: `HealthStartupCmd`, `HealthStartupInterval`, `HealthStartupRetries` (attempts before the container is restarted), `HealthStartupSuccess` (successful runs required before the regular check begins), `HealthStartupTimeout`.

Logs: `HealthLogDestination` is a directory path, `local` (default, kept in overlay containers) or `events_logger`; a directory gets a file named `<container-ID>-healthcheck.log`. `HealthMaxLogCount` defaults to 5 attempts (0 is infinite) and `HealthMaxLogSize` to 500 characters (0 is infinite).

`Notify=healthy` postpones the systemd startup notification until Podman healthchecks mark the container healthy; it requires a configured healthcheck (see `HealthCmd`).


Example values from the table: `HealthCmd=/usr/bin/command`, `HealthInterval=2m`, `HealthRetries=5`, `HealthStartPeriod=1m`, `HealthTimeout=20s`, `HealthOnFailure=kill`, `HealthStartupCmd=command`, `HealthStartupInterval=1m`, `HealthStartupRetries=8`, `HealthStartupSuccess=2`, `HealthStartupTimeout=1m33s`, `HealthLogDestination=/foo/log`, `HealthMaxLogCount=5`, `HealthMaxLogSize=500`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
