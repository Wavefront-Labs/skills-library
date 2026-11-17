---
id: computing-software.database-administration.patroni.patroni-systemd-integration
name: patroni-systemd-integration
category: computing-software
field: database-administration
product: patroni
tags: [patroni, systemd, notify, sighup, service]
level: advanced
status: docs-checked
description: "Documented systemd behaviour: Type=notify, notify-reload, NOTIFY_SOCKET handling and restart cautions."
sources:
  - https://patroni.readthedocs.io/en/latest/releases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Patroni under systemd without surprises.

From the release notes:
- 4.1.0 added support for the systemd `notify` unit type. Without it, you could start Patroni and immediately send SIGHUP via systemd, killing it before it set up its signal handlers.
- 4.1.2 added `notify-reload` unit type support, so `systemctl reload` waits until Patroni has processed the reload (it sends `RELOADING=1` and `READY=1`), and Patroni sends `STOPPING=1` on shutdown. `NotifyAccess=all` was removed from the example unit file, and `NOTIFY_SOCKET` is filtered from the environment when starting PostgreSQL, so Postgres does not send `READY=1` or `STOPPING=1` itself. When taking over a Postgres started earlier with `NOTIFY_SOCKET`, Patroni re-asserts `READY=1` during PostgreSQL shutdown.
- 4.1.3 includes `MONOTONIC_USEC` in the `RELOADING=1` notification because systemd 257+ requires it for `Type=notify-reload`; without it, `systemctl reload` hangs. It also warns about running under systemd without the python-systemd package only when `NOTIFY_SOCKET` is present.
- 4.1.4 imports the systemd package only when `NOTIFY_SOCKET` is set, avoiding a FileNotFoundError.

FAQ guidance: reload local config with `systemctl reload PATRONI_UNIT.service`, or `kill -s HUP PID` otherwise. Do not leave the `postgresql.service` unit enabled; Patroni alone must start, stop and promote Postgres, otherwise a restarted failed primary can cause split-brain. Restarting the Patroni service on a primary can trigger a failover.

## Checked

2026-11-03. Confirmed against the release notes entries for 4.1.0, 4.1.2, 4.1.3 and 4.1.4 and the FAQ guidance on `systemctl reload` and the postgresql.service unit.

Method: documentation only; no commands were run.
