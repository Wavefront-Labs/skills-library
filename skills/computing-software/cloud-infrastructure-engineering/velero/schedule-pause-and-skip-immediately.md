---
id: computing-software.cloud-infrastructure-engineering.velero.schedule-pause-and-skip-immediately
name: schedule-pause-and-skip-immediately
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [schedule-paused, skipimmediately, lastskipped, pause-schedule, schedule-control]
level: practitioner
status: docs-checked
description: "Use the Schedule paused and skipImmediately fields and the lastSkipped status to control when a Velero schedule next runs."
sources:
  - https://velero.io/docs/main/api-types/schedule/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Schedule API has three fields that control execution, all in `velero.io/v1`.

`spec.paused`: when `true`, no new backups are created. Set it back to `false` and the schedule resumes on its cron expression.

`spec.skipImmediately`: by default (`false`), if a backup is due immediately when a schedule is created or unpaused, it runs right away. Set `true` to suppress that first run. The controller then:
1. Skips the immediate backup.
2. Records the current time in `status.lastSkipped`.
3. Resets `skipImmediately` to `false` (one-time use).
4. Computes the next backup from the cron expression using `lastSkipped` as the reference time.

`status.lastSkipped`: read-only; you cannot set it. The controller uses it, when more recent than `lastBackup`, to calculate the next scheduled time.

The "consume and reset" pattern means you do not need to flip the flag back yourself; later runs behave normally.

Typical use: set `paused: true` during a maintenance window or a restore, then unpause with `skipImmediately: true` so resuming does not fire a backup straight away.

Schedule objects must live in the namespace of the Velero server.

## Checked

2026-11-08. Read in full: the Schedule API Type page. Every remaining claim was confirmed there. Removed or reworded: nothing.

Method: documentation only; no commands were run.
