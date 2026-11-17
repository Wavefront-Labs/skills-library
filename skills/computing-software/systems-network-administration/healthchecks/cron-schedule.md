---
id: computing-software.systems-network-administration.healthchecks.cron-schedule
name: cron-schedule
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, cron-schedule, cron-expression, server-time-zone, tz-parameter]
level: practitioner
status: docs-checked
description: "Set up a Healthchecks cron schedule using the crontab expression and server time zone, including the API schedule and tz fields and a timezone mismatch check."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_cron_jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A cron schedule verifies jobs run at the right time of day, not merely at the right interval.

Fields:
- Cron Expression: the same expression as in the crontab.
- Server's Time Zone: set it when the server is not on UTC, because cron normally uses local system time.
- Grace Time: as for simple schedules.

API: pass `schedule` and `tz` (default `UTC`; `tz` only applies with `schedule`). For example:

```
{"schedule": "0,30 * * * *", "tz": "Europe/Riga"}
```

Behaviour: the check goes late at the scheduled time if no ping has arrived (e.g. `10 * * * *` is expected at minute 10 each hour).

If pings consistently look an hour early or late, the server and check time zones differ. Inspect the server with `timedatectl status` and read the `Time zone:` line.

Look at cron's own logs on systemd hosts:

```
journalctl --since "1 hour ago" -t CRON
```

For systemd timers use an OnCalendar schedule instead.

## Checked

2026-11-04: confirmed against the Configuring Checks page (cron fields, server time zone), the Management API page (schedule, tz default UTC, Europe/Riga) and the Monitoring cron jobs page (timedatectl status, journalctl -t CRON). The late-at-scheduled-time example is from the introduction page.
Method: documentation only; no commands were run.
