---
id: computing-software.data-engineering.databricks.job-notifications-and-duration-thresholds
name: job-notifications-and-duration-thresholds
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, job-notifications, duration-threshold, streaming-backlog-alerts, notification-destinations, slack-alerts, pagerduty, timeouts]
level: practitioner
status: docs-checked
description: "Alert on Databricks jobs: email and destination notifications, duration warnings, streaming backlog rules, timeouts and noise suppression."
sources:
  - https://docs.databricks.com/aws/en/jobs/notifications
  - https://docs.databricks.com/aws/en/admin/workspace-settings/notification-destinations
  - https://docs.databricks.com/aws/en/jobs/configure-job#timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job notifications and duration thresholds

**Goal:** the right people hear about failures and slow runs immediately, and nobody learns to ignore alerts.

## 1. Notification destinations
Admins create destinations once (Settings > Workspace admin > Notifications tab): Slack, Microsoft Teams, PagerDuty and generic webhook, plus email addresses. A job or task can use at most three system destinations per notification event type. Webhook payloads (event types such as `jobs.on_failure`) are defined by the receiving service's format; Slack and Teams message content may change, so use a user-defined webhook if you need a stable schema.

## 2. Job-level configuration
```yaml
email_notifications:
  on_failure: [data-oncall@example.com]
  on_duration_warning_threshold_exceeded: [data-oncall@example.com]
webhook_notifications:
  on_failure: [{id: <pagerduty-destination-id>}]
  on_duration_warning_threshold_exceeded: [{id: <slack-destination-id>}]
  on_streaming_backlog_exceeded: [{id: <slack-destination-id>}]
notification_settings:
  no_alert_for_skipped_runs: true
  no_alert_for_canceled_runs: true
health:
  rules:
    - {metric: RUN_DURATION_SECONDS, op: GREATER_THAN, value: 5400}
timeout_seconds: 10800
```
- Events: `on_start`, `on_success`, `on_failure`, `on_duration_warning_threshold_exceeded`, `on_streaming_backlog_exceeded`.
- Task-level notifications exist too; use them only when a task has a different owner.
- Job-level notifications are not sent when failed tasks are retried; use task notifications (optionally "Mute notifications until the last retry") for per-task failure alerts. Tasks are retried three times by default.
- A run that finishes "Succeeded with failures" counts as successful; select Success to be told about it.

## 3. Duration thresholds vs timeouts
- **Duration warning** (health rule `RUN_DURATION_SECONDS`) — notifies, run continues. Set at ~1.5-2x the normal p95 duration so a stuck run is noticed before the SLA is missed.
- **Timeout** (`timeout_seconds` on job or task) — kills the run. Set above the worst legitimate duration; stops runaway costs. Combine with `retry_on_timeout` only if retrying can help.

## 4. Streaming backlog rules
For continuous / streaming tasks:
```yaml
health:
  rules:
    - {metric: STREAMING_BACKLOG_SECONDS, op: GREATER_THAN, value: 900}
    - {metric: STREAMING_BACKLOG_FILES, op: GREATER_THAN, value: 10000}
```
Also `STREAMING_BACKLOG_BYTES` and `STREAMING_BACKLOG_RECORDS`. Notifications fire when the average backlog over a 10-minute period exceeds the threshold, then repeat at 30-minute intervals while it stays high. They are not supported for pipeline tasks and need the Jobs service to track the streaming query, so do not use `awaitTermination()` in the job.

## 5. Alert hygiene
- Page (PagerDuty) only for jobs with a business SLA; send the rest to a channel.
- Suppress alerts for skipped and cancelled runs.
- Every alerting job has an owner and a runbook link in its description (`description:` field or tags).
- Review monthly: jobs that alerted >N times without action need fixing or downgrading.

## Verify
- [ ] Forcing a task failure sends exactly one alert to the right destination after retries.
- [ ] A run exceeding the duration threshold sends a warning but keeps running.
- [ ] Timeouts are set on every scheduled job.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: notification events including duration and streaming backlog, the three-destination limit, retry behaviour of job-level notifications, mute options for skipped and canceled runs, backlog averaging and 30-minute repeat, the awaitTermination caveat, and the admin Notifications tab location (notifications and notification-destinations pages). The health-rule and notification-settings field names matched in the fetched job pages by phrase search only.

Removed or corrected: the claim that jobs reference destinations by ID without URLs, the "after retries are exhausted" wording (job-level alerts are simply not sent on retries), the per-source backlog metric support list, and the incorrect Settings path. Duration and alert-hygiene thresholds are advice, not documented limits.

Method: documentation only; no commands were run.
