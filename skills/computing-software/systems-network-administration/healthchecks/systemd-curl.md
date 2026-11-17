---
id: computing-software.systems-network-administration.healthchecks.systemd-curl
name: systemd-curl
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, systemd-service, execstartpre, execstoppost, exit-status-variable]
level: practitioner
status: docs-checked
description: "Monitor a systemd service with Healthchecks using curl in ExecStartPre and ExecStopPost to send start and exit-status signals."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_systemd_tasks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each scheduled task has a `.service` file (command, user, environment) and a `.timer` file (schedule). Add these lines to the `[Service]` section:

```
[Service]
Type=oneshot
ExecStart=rsync -a /opt/media/ remote_user@remote_host:/opt/media/
ExecStartPre=-curl -sS -m 10 --retry 5 <ping-url>/start
ExecStopPost=curl -sS -m 10 --retry 5 <ping-url>/${EXIT_STATUS}
```

How it works:
- `ExecStartPre` sends the start signal before the main command.
- The leading `-` tells systemd to ignore a curl failure, so the task still runs.
- `ExecStopPost` runs after the main command and reports its exit status. Healthchecks treats 0 as success and any higher value as failure.
- `-sS` shows errors only, `-m 10` is a 10 second timeout, `--retry 5` retries transient failures.

This catches machine outages, invalid systemd configuration, non-zero exits and tasks running at the wrong time or too long.

Limit: the curl method does not capture command output (use runitor, see systemd-runitor).

Match the schedule with an OnCalendar check (see oncalendar-schedule).

## Checked

2026-11-04: confirmed against the Monitoring systemd tasks page (ExecStartPre with the - prefix, ExecStopPost with EXIT_STATUS, curl flags, failure modes, no output capture). Removed a remark about undocumented behaviour of the ExecStopPost curl.
Method: documentation only; no commands were run.
