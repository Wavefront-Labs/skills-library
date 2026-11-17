---
id: computing-software.collaboration-platform-administration.zulip.logs-and-supervisorctl
name: logs-and-supervisorctl
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [zulip-logs, supervisorctl, restart-server, errors-log]
level: practitioner
status: docs-checked
description: "Find Zulip logs under /var/log/zulip and manage services with supervisorctl status, restart-server and stop-server, including when not to use supervisorctl restart."
sources: ["https://zulip.readthedocs.io/en/latest/production/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zulip logs and supervisorctl

Start every investigation in `/var/log/zulip/`. It has one file per service plus:

- `errors.log`: all errors; check this first.
- `server.log`: Django and Tornado logs (a search tool for it exists).
- `workers.log`: combined queue worker logs.
- `install.log` and `upgrade.log`: installer and upgrade transcripts.

Zulip's Python services run under Supervisor. The service list is defined in `/etc/supervisor/conf.d/zulip.conf` and `/etc/supervisor/conf.d/zulip-db.conf`. Run `supervisorctl status` to check them. Healthy output lists entries such as `zulip-django`, `zulip-tornado`, `smokescreen`, `process-fts-updates`, `zulip_deliver_scheduled_emails` and a group of `zulip-workers:zulip_events_*` workers, all `RUNNING`.

A status other than `RUNNING`, or an uptime under 5 seconds, means the service is crash-looping. If `errors.log` shows nothing, read the file named by `stdout_logfile` in that service's entry in `zulip.conf`; messages only reach `errors.log` once a service has started fully.

Restarting: use `~zulip/deployments/current/scripts/restart-server` after changing `/etc/zulip/settings.py`. A config file can be shared by several services, so `supervisorctl restart zulip-django` for one service is only for when you are sure that is all that needs it, and it can cause inconsistent behaviour for settings changes. Stopping everything is `scripts/stop-server`; individual services use `supervisorctl stop <name>`.

In Docker, supervisorctl runs inside the container.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/troubleshooting.html (zulip.readthedocs.io, latest). Removed: the 'run as root' wording for supervisorctl status.

Method: documentation only; no commands were run.
