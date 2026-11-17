---
id: computing-software.data-engineering.databricks.job-triggers-file-arrival-and-table-update
name: job-triggers-file-arrival-and-table-update
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, file-arrival-trigger, table-update-trigger, scheduled-trigger, continuous-job, event-driven-pipelines, quartz-cron]
level: practitioner
status: gated
description: "Trigger Databricks jobs by schedule, file arrival, table update or continuously: configuration, throttling settings, limits, and choosing event triggers over polling schedules."
sources:
  - https://docs.databricks.com/aws/en/jobs/triggers
  - https://docs.databricks.com/aws/en/jobs/file-arrival-triggers
  - https://docs.databricks.com/aws/en/jobs/trigger-table-update
  - https://docs.databricks.com/aws/en/jobs/scheduled
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job triggers: schedule, file arrival, table update, continuous

**Goal:** jobs run when their inputs are ready, not on a clock that guesses when upstream finishes.

## 1. Trigger types
| Trigger | Fires when | Typical use |
|---|---|---|
| Scheduled | Quartz cron (`0 0 3 * * ?`) in a timezone | daily batch with fixed SLA |
| File arrival | new files appear in a UC external location or volume path | partner file drops |
| Table update | one or more UC tables are updated | downstream jobs chained on data, across teams |
| Continuous | always running; new run starts when the previous ends | streaming jobs |

## 2. File arrival
```yaml
trigger:
  pause_status: UNPAUSED
  file_arrival:
    url: /Volumes/prod/landing/partner_x/        # or s3://bucket/path/ under an external location
    min_time_between_triggers_seconds: 300        # throttle
    wait_after_last_change_seconds: 120           # wait for multi-file drops to finish
```
- The job owner/run-as needs `READ FILES` on the external location or `READ VOLUME`.
- Checked on a best-effort basis about every minute; without file events enabled on the external location there is a cap on how many files the monitored path may contain (see docs) — enable file events or keep the landing path tidy (move processed files).
- The trigger only starts the job; the job must still find which files are new — use Auto Loader / COPY INTO inside it.
- The YAML field names in this section come from the Jobs API schema (gated: unconfirmed, source is paywalled or blocked).

## 3. Table update
```yaml
trigger:
  table_update:
    table_names: [prod.silver.orders, prod.silver.customers]
    condition: ALL_UPDATED            # or ANY_UPDATED
    min_time_between_triggers_seconds: 600
    wait_after_last_change_seconds: 300
```
Decouples producer and consumer jobs (different teams, different bundles) without cross-job dependencies.
`ALL_UPDATED` waits until every listed table changed since the last run.

## 4. Schedules done right
- Always set `timezone_id` explicitly; DST shifts local times.
- Avoid the top-of-hour stampede: `0 7 3 * * ?` instead of `0 0 3`.
- Use `pause_status: PAUSED` in non-prod targets (bundles dev mode does this).
- Check the maximum concurrent runs setting: with 1, a scheduled run is skipped while the previous one is still running (gated: unconfirmed, source is paywalled or blocked).

## 5. Continuous jobs
```yaml
continuous: {pause_status: UNPAUSED}
```
Do not combine with a schedule. Use for Structured Streaming tasks.

## Verify
- [ ] Dropping a test file triggers exactly one run after the wait period.
- [ ] Downstream job runs only after all upstream tables update (for `ALL_UPDATED`).
- [ ] Schedules have explicit time zones and are paused outside prod.

## Checked

2026-10-28. Confirmed: the file arrival trigger checks about every minute, best effort, on the file arrival trigger page. Removed: an unconfirmed retry/backoff claim.

Method: documentation only; no commands were run.
