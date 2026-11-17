---
id: computing-software.collaboration-platform-administration.zulip.zulip-conf-application-server-tuning
name: zulip-conf-application-server-tuning
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [application-server, uwsgi-processes, nginx-server-name, queue-workers]
level: advanced
status: docs-checked
description: "Tune the [application_server] section of zulip.conf: nginx workers, server_name, uwsgi processes, queue worker modes, rolling restarts, file descriptors and KaTeX."
sources: ["https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tuning [application_server] in zulip.conf

Frequently useful keys:

- `nginx_server_name`: set `server_name` on Zulip's nginx blocks when other software shares the host. List every hostname, including those on its certificate, space-separated, or certificate renewal fails. Wildcards work, such as `example.com *.example.com`.
- `nginx_worker_processes` (default `auto`) and `nginx_worker_connections` (default 10000). Their product should exceed twice the concurrent users.
- `uwsgi_processes`: Django workers, scaling from 3 on hosts under 3 GB RAM to 16 above 24 GB. `uwsgi_listen_backlog_limit` overrides the 128 backlog.
- `queue_workers_multiprocess`: normally auto-detected from memory (about 3.5 GiB threshold); multithreaded mode saves 1.5 GiB. Override in Docker, where the host's memory is seen, and when services are on remote servers.
- `dedicated_soft_reactivation_queue` and `dedicated_deferred_work_high_latency_queue` split slow jobs (exports, Slack imports, deletion of deactivated organizations) from `deferred_work`. Apply with `zulip-puppet-apply` then restart. To disable the latter, set false, restart, wait until `rabbitmqctl list_queues` shows `deferred_work_high_latency` empty, then apply, or queued jobs are never processed.
- `rolling_restart`: restarts uwsgi one at a time, fewer 502s, mixed code versions briefly.
- `service_file_descriptor_limit`: default 40000.
- `thumbnail_workers` and `email_senders_workers`: default 1.
- `access_log_retention_days`: default 14.
- `katex_server` and `katex_server_port` (9700): disabling saves memory but makes math slow.
- `custom_ca_path`: PEM CA for your auth provider; switches Zulip to the OS CA store.

## Checked

2026-11-08. Checked: commands, paths, flags, settings and figures read against the Zulip system-configuration page (docs/production/system-configuration.md in the zulip repository, read in full). Removed: nothing.

Method: documentation only; no commands were run.
