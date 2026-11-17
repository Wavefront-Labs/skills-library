---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-job-scheduling-chaining-and-windows
name: veeam-job-scheduling-chaining-and-windows
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam, job-chaining, backup-window, job-scheduling, retry-policy, backup-copy]
level: practitioner
status: docs-checked
description: "Schedule Veeam jobs: daily, monthly, periodic and after-job options, permitted time windows, start offset and how periodic intervals are counted."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_job_schedule_vm.html
  - https://bp.veeam.com/vbr/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job scheduling and chaining (Veeam)

At the Schedule step of the job wizard, select **Run the job automatically** (otherwise start it manually), then one option:
- **Daily at this time:** a set time, on weekdays or on chosen days.
- **Monthly at this time:** once a month on chosen days.
- **Periodically every:** repeats through the day at a set interval. Choosing *Continuously* starts a new session as soon as the previous one finishes. Click **Schedule** to set the permitted time window (Time Periods window); *Start time within an hour* shifts the schedule by an offset (prohibited 08:00-10:00 with offset 25 becomes 08:00-10:25).
- **After this job:** chains the job after a selected one. Define the time schedule only for the first job in the chain; for the others choose After this job and pick the preceding job.

## How periodic schedules start
- Intervals are counted from 12:00 AM (a 4-hour interval runs at 12:00 AM, 4:00 AM, 8:00 AM and so on).
- With permitted hours, the job starts immediately when the denied interval ends, then follows the schedule. Example from the guide: 2-hour interval with permitted hours 9:00 AM-5:00 PM runs at 9:00, 10:00, 12:00, 2:00 PM and 4:00 PM.

## Chaining
The guide points to a separate "Chained Jobs" page for recommendations; this page was not read. The Veeam Best Practice Guide (bp.veeam.com) is the place to look for advice on chaining versus parallel scheduling.

## Checked
Date: 2026-11-03. Confirmed against the Veeam Help Center page "Step 11. Define Job Schedule" (read in part; truncated after the daylight-saving note).
Removed (not on the page): retry defaults (3 times, 10 minutes), the "terminate job if it exceeds the backup window" option, the claim that chaining is worse than parallel scheduling, staggering numbers, concurrent-task and I/O-control advice, time-zone and disabled-job remarks, backup copy mode notes, Verify section.
Method: documentation only; no commands were run.
