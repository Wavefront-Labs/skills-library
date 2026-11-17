---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-notify-and-reload
name: quadlet-container-notify-and-reload
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, notify, sd-notify, reloadcmd, reloadsignal, stopsignal, stoptimeout]
level: advanced
status: docs-checked
description: "Control Quadlet startup notification with Notify=true or healthy, and add systemctl reload using ReloadCmd or ReloadSignal, plus StopSignal and StopTimeout."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tell systemd accurately when the container is ready, reloadable and stopped.

`Notify=` defaults to false: the container runtime handles the systemd notify, so the service counts as started when the runtime starts the child. If the application supports sd_notify, `Notify=true` passes the notification details into the container so it signals startup itself (the table maps this to `--sdnotify container`). `Notify=healthy` delays notification until the Podman healthcheck marks the container healthy, so a healthcheck must be configured.

Reload: `ReloadCmd=` adds an `ExecReload` line that runs `podman exec` with the command in the container. `ReloadSignal=` adds an `ExecReload` that runs `podman kill` with the signal against the main container process. They are mutually exclusive. Trigger either with `systemctl reload <Service>`.

Stopping: `StopSignal=` sets the stop signal (default SIGTERM); `StopTimeout=` maps to `--stop-timeout`.

`RunInit=true` (`--init`, default false) adds a minimal init in the container that forwards signals and reaps processes.


`StopTimeout=20` is the page's example for the stop timeout and `StopSignal=SIGINT` for the stop signal.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
