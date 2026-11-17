---
id: computing-software.messaging-and-integration.temporal.cron-jobs-legacy
name: cron-jobs-legacy
category: computing-software
field: messaging-and-integration
product: temporal
tags: [cron-job, cron-schedule, cron-tz, firstworkflowtaskbackoff, daylight-saving, robfig]
level: practitioner
status: docs-checked
description: "Temporal Cron Jobs: cron schedule on workflow start, firstWorkflowTaskBackoff, CRON_TZ time zones and DST traps, how to stop one; Schedules are recommended instead."
sources:
  - https://docs.temporal.io/cron-job
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Schedules are the recommended replacement for Cron Jobs (more options, updatable, pausable). A Cron Job is the series of runs created when a cron schedule is passed while starting a workflow.

Behaviour: each run gets the same input and options as the first. The Server creates the first run immediately but applies a `firstWorkflowTaskBackoff` so its first Workflow Task is not queued until the scheduled time. The next run is created only after the current one completes, fails or hits the Workflow Run Timeout; if a Retry Policy exists, retries finish first. If the next slot arrives while a run is open, it starts after that run completes successfully, with the backoff computed from its start time.

Format: UTC by default. Classic five fields (minute 0-59, hour 0-23, day of month 1-31, month 1-12, day of week 0-6); `15 8 * * *` is daily 08:15 UTC. Also robfig predefined values `@yearly`/`@annually`, `@monthly`, `@weekly`, `@daily`/`@midnight`, `@hourly`, and `@every <duration>` (Go `time.ParseDuration`).

Time zones (Temporal 1.15+): prefix `CRON_TZ=America/New_York 15 8 * * *`. UTC is strongly recommended. Traps:
- Around DST changes (such as `30 2 * * *`) a job can run zero, one or two times; some zones skip midnight.
- The next run's absolute time is stored when the previous run completes and never recomputed, so a rare job may fire wrong after a zone definition change.

Stopping: runs continue until the workflow is terminated or the Workflow Execution Timeout is reached.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: cron-job (under https://docs.temporal.io/). Nothing removed.

Method: documentation only; no commands were run.
