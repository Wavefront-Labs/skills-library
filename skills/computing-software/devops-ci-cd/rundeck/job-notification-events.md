---
id: computing-software.devops-ci-cd.rundeck.job-notification-events
name: job-notification-events
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, job-notifications, avg-duration, notification-events, option-reference]
level: practitioner
status: docs-checked
description: "Choose Rundeck job notification events (start, success, failure, retryable failure, average duration exceeded) and set duration thresholds."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-notifications.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Notifications fire on job events, and each uses a chosen notification plugin (email, webhook and others).

Events:
- Start: all start notifications fire when the job starts.
- On Success: fires when the job finishes successfully.
- On Failure: fires if the job fails or is cancelled.
- On Retryable Failure: fires for retryable failure notifications when the job fails.
- Average Duration Exceeded: fires when a threshold is exceeded; if none is given, the job's average duration is used.

Threshold formats:
- Percentage of average: `20%`
- Time delta from average: `+20s`, `+20`
- Absolute time: `30s`, `5m`

Units are s, m, h, d, w, y; with no unit the value is seconds. Thresholds can include option references such as `${option.avgDurationThreshold}`.

Configure:
1. Open the job's Notifications tab.
2. Choose the event and click `+ Add Notification`.
3. Pick the Notification Type and fill in that plugin's settings.

Verify by triggering each event (for example abort a run to test On Failure).

## Checked

2026-11-04. Confirmed against the Rundeck docs page Job Notifications: the five events and their wording, the Average Duration Exceeded threshold formats (20%, +20s, +20, 30s, 5m), unit letters s m h d w y with seconds as the default, option references, and the Notifications tab and + Add Notification steps. Nothing removed.

Method: documentation only; no commands were run.
