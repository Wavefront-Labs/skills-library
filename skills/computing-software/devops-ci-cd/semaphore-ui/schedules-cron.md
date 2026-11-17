---
id: computing-software.devops-ci-cd.semaphore-ui.schedules-cron
name: schedules-cron
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [schedules, cron, timezone, automation, recurring, semaphore-ui]
level: practitioner
status: docs-checked
description: "Run templates on a cron schedule, set the schedule timezone, and attach alerts."
sources:
  - https://semaphoreui.com/docs/user-guide/schedules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Schedules

Goal: automate runs at fixed times.

Timezone defaults to UTC. Change it in the config or environment, then restart Semaphore:

```json
{ "schedule": { "timezone": "America/New_York" } }
```

or `export SEMAPHORE_SCHEDULE_TIMEZONE="America/New_York"` (IANA names).

Create: Schedule tab, New Schedule. Fields: Name, Template, Timing (cron expression or built-in intervals), and optional alerts (the template's alerts or a different project alert set).

Cron uses five fields: minute, hour, day of month, month, day of week (Sunday=0).

- `*/15 * * * *` every 15 minutes
- `0 2 * * *` 02:00 daily
- `0 0 * * 0` midnight Sundays
- `0 9 1 * *` 09:00 on the first of each month

Uses on the page: system updates (weekly, off-hours), backups, compliance checks, and scheduled creation and teardown of test environments.

Schedules can pass parameters to tasks: enable prompts for the needed fields in the template, then define the values in the schedule.

Tip from the page: test schedules with short intervals before setting up production schedules with longer ones.

## Checked

2026-11-07. Read in full: the Schedules page, from its markdown source in the semaphore-docs repository (user-guide/schedules.md; no snippet files included). Confirmed: UTC default, the schedule.timezone key and SEMAPHORE_SCHEDULE_TIMEZONE, the restart note, the Schedule tab and New Schedule button, the Name, Template and Timing fields, the alerts choice, the five cron fields and the four examples, and the task-parameters paragraph. Removed: repository-polling use, survey-variable passing, the browser-timezone claim, the audit-log trigger remark, and the next-task Verify step.
Method: documentation only; no commands were run.
