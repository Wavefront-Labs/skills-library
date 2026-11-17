---
id: computing-software.systems-network-administration.healthchecks.systemd-runitor
name: systemd-runitor
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, runitor, command-wrapper, captured-output]
level: practitioner
status: docs-checked
description: "Wrap a systemd ExecStart command with runitor so Healthchecks start, success and failure signals and captured output are sent automatically."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_systemd_tasks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
runitor is a third-party command runner (github.com/bdd/runitor). It sends the start, success and failure signals itself and captures and truncates command output, which the plain curl method cannot do.

In the service unit:

```
ExecStart=runitor -uuid your-uuid-here -- rsync -a /opt/media/ remote_user@remote_host:/opt/media/
```

Replace `your-uuid-here` with the check's UUID.

Notes:
- The runitor binary must be in the system PATH.
- Everything after `--` is the command to run.
- Other command runners and wrappers listed in the Healthchecks resources page: crontask.sh (Bash crontab wrapper), task-mon (small Rust binary), hc-monitor (Bash wrapper gist) and pytocron (Python cron implementation).

Pair with a timer using `OnCalendar=` and a Healthchecks OnCalendar schedule.

## Checked

2026-11-04. Confirmed against the Healthchecks Monitoring Systemd Tasks and Third-Party Resources pages: runitor's role, capturing and truncating output, the ExecStart example, the PATH requirement, the other command runners listed, and native OnCalendar schedules. Removed a statement about exit status handling under runitor, which the page gives only for the curl method.

Method: documentation only; no commands were run.
