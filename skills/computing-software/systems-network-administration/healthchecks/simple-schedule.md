---
id: computing-software.systems-network-administration.healthchecks.simple-schedule
name: simple-schedule
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, simple-schedule, period, interval-checks]
level: intro
status: docs-checked
description: "Configure a Healthchecks simple schedule with a period and grace time for jobs that run at roughly regular intervals such as hourly, daily or weekly."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use a simple schedule for processes that run at roughly regular intervals (hourly, daily, weekly) where the exact time of day does not matter.

Settings:
- Period: the expected time between pings.
- Grace Time: extra time before alerting on a late check. With start signals it also caps the gap between start and success.

Through the Management API, a simple check is defined with `timeout` (the period) and `grace`, each in seconds in the range 60 to 31536000. If `schedule` is also supplied, it overrides `timeout`.

```
{"name": "Backups", "timeout": 300}
```

Choose a simple schedule when drift is fine. If the job must run at a specific time (for example 02:00 daily), use a cron or OnCalendar schedule, which ensures the job runs at the correct time and not just at the correct intervals.

Newly auto-provisioned checks start as period 1 day and grace 1 hour.

## Checked

2026-11-04: confirmed against the Configuring Checks page (Period, Grace Time, start-signal note), the Management API page (timeout and grace 60 to 31536000 seconds, schedule takes precedence over timeout) and the Auto Provisioning page (defaults). Reworded the cron remark to match the page.
Method: documentation only; no commands were run.
