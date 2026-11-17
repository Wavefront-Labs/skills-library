---
id: computing-software.systems-network-administration.healthchecks.grace-time
name: grace-time
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, grace-time, late-vs-down, alert-delay]
level: practitioner
status: docs-checked
description: "How Healthchecks grace time turns a late check into a down check for simple and cron schedules, and how it also bounds start-to-success run time."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/introduction.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/monitoring_cron_jobs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Grace time is the extra wait before an alert is sent. It absorbs normal timing variation.

Simple schedule: the check becomes late when the period has passed since the last ping. Example: period 1 hour, grace 5 minutes, last ping 12:00. At 13:00 it is Late; at 13:05 it is Down and alerts are sent.

Cron or OnCalendar schedule: the check becomes late at the exact scheduled time with no ping. Example: schedule `10 * * * *`, grace 5 minutes, last ping 12:30. At 13:10 Late; at 13:15 Down.

With start signals: grace time is also the maximum gap between start and success. No success within it means the run failed and alerts are sent.

Sizing: set grace above the job's normal duration. Example from the docs: a daily 14:00 job taking 15 to 25 minutes gets a 30 minute grace; no ping by 14:30 marks it failed.

Email pings are subject to random delivery delays, so use a longer grace for them.

## Checked

2026-11-04: confirmed against the introduction page (both worked examples, start-signal rule), the Monitoring cron jobs page (14:00 job, 30 minute grace) and the Email page (random delivery delays).
Method: documentation only; no commands were run.
