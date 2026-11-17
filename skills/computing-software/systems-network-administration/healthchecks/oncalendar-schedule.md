---
id: computing-software.systems-network-administration.healthchecks.oncalendar-schedule
name: oncalendar-schedule
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, oncalendar-schedule, systemd-timer, multiple-expressions]
level: practitioner
status: docs-checked
description: "Use systemd OnCalendar expressions as a Healthchecks schedule, including multiple expressions per check and the API schedule field."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_systemd_tasks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OnCalendar schedules match systemd timers that use `OnCalendar=`. Copy the expression from the `.timer` file straight into the check's schedule; Healthchecks accepts the same syntax.

Timer example from the docs (every 4 hours on workdays):

```
[Timer]
OnCalendar=Mon-Fri *-*-* 0/4:00
```

Rules:
- You may enter several expressions, one per line; a ping is expected whenever any of them matches.
- OnCalendar is not cron syntax. Write it in systemd's format (see systemd.time(7)).
- Via the Management API, pass it in the `schedule` field (with `tz`). The docs show an example for 12:00 on the last day of each month.
- `schedule` overrides `timeout` if both are given.

Lateness works like cron schedules: the check goes late at the exact scheduled time if no ping has arrived, then down after the grace time.

Pair the timer's service unit with start and exit-status pings (see systemd-curl).

## Checked

2026-11-04: confirmed against the Configuring Checks page (OnCalendar, several expressions one per line), the Monitoring systemd tasks page (the OnCalendar=Mon-Fri *-*-* 0/4:00 timer) and the Management API page (schedule, tz, schedule over timeout, last-day-of-month example). Late then down timing is from the introduction page.
Method: documentation only; no commands were run.
