---
id: computing-software.collaboration-platform-administration.zulip.monitoring-zulip-nagios
name: monitoring-zulip-nagios
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [monitoring, nagios-plugins, check-send-receive-time, rabbitmq-queues-check]
level: advanced
status: docs-checked
description: "Monitor a Zulip server: error emails to ZULIP_ADMINISTRATOR, host and service checks, supervisorctl status, OOM kills, and bundled Nagios plugins like check_send_receive_time."
sources: ["https://zulip.readthedocs.io/en/latest/production/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring a Zulip server

Zulip emails Django error reports to `ZULIP_ADMINISTRATOR` for backend exceptions. A healthy server should send none, so investigate or report any.

Standard monitoring still applies:

- Disk space, especially for the database and wherever uploads live.
- Uptime of nginx, PostgreSQL, Redis, RabbitMQ and memcached, using your monitoring software's usual plugins.
- `supervisorctl status` with every service `RUNNING`.
- Processes killed by the OOM killer.

Zulip also ships application-level Nagios plugins, installed under subdirectories of `/usr/lib/nagios/plugins/`:

- `check_send_receive_time`: sends a test message between two bot users, a good end-to-end test of Django and Tornado.
- `check_rabbitmq_consumers` and `check_rabbitmq_queues`: health of the RabbitMQ queueing system. Together with the first, they usually point to the cause of any production issue.
- `check_worker_memory`: watches queue workers for memory leaks.
- `check_fts_update_log`: detects full-text search updates backlogging.
- `check_postgres`: general database health.
- `check_postgresql_replication_lag`: whether streaming replication is current.
- `check_debian_packages`: whether the system is behind on apt upgrades.

The full Nagios configuration used for the project's own servers (without secrets) lives in the Git repository, not in release tarballs.

As a memory leak safeguard, Zulip restarts itself early every Sunday; the schedule is in `/etc/cron.d/restart-zulip`.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/troubleshooting.html (zulip.readthedocs.io, latest). Removed: the uptime-graph advice.

Method: documentation only; no commands were run.
