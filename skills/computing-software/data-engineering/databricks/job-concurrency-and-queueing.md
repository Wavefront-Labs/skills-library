---
id: computing-software.data-engineering.databricks.job-concurrency-and-queueing
name: job-concurrency-and-queueing
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, job-queueing, max-concurrent-runs, lakeflow-jobs, concurrency]
level: practitioner
status: docs-checked
description: "Control Databricks job concurrency: max_concurrent_runs, run queueing when limits are hit, overlapping schedules, and patterns for safe parallel runs."
sources:
  - https://docs.databricks.com/aws/en/jobs/advanced#configure-maximum-concurrent-runs
  - https://docs.databricks.com/aws/en/jobs/settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job concurrency limits and queueing

**Goal:** jobs never run twice on top of each other unless designed to, and runs are not dropped when capacity is temporarily exhausted.

## Settings
```yaml
resources:
  jobs:
    orders_hourly:
      max_concurrent_runs: 1          # default 1
      schedule:
        quartz_cron_expression: "0 0 * * * ?"
        timezone_id: UTC
```
- With `max_concurrent_runs: 1` and queueing on, a run triggered while one is active waits in the queue; with queueing off it can be **skipped**. Turn queueing on with the Queue toggle under Advanced settings (it is on by default for jobs created in the UI after April 15, 2024).
- A run is queued when the workspace limit on concurrent active runs, the workspace limit on concurrent Run Job task runs, or the job's maximum concurrent runs is reached. Queueing is a job-level property.
- A run waits in the queue for up to 48 hours if resources are unavailable; queued runs show in the job's runs list.

## Parallel runs by design
For parameterised jobs (one run per country/date), raise `max_concurrent_runs` and make tasks write to disjoint partitions or use idempotent MERGE with partition predicates to avoid Delta concurrent-write conflicts.

## Long runs vs schedule
If runs take longer than the interval, queueing builds a backlog. Set a duration threshold on the job to alert and fix duration, or switch to a continuous/file-arrival trigger.

## Gotchas
- New jobs default to a maximum of 1 concurrent run.

## Verify
Trigger two runs back to back: the second shows Queued and starts when the first ends.

## Checked

- 2026-10-28: confirmed on the job settings page (queueing, 48-hour wait, queue limits, default maximum concurrent runs of 1, duration thresholds) and the bundle resources page (`max_concurrent_runs`, `quartz_cron_expression`, `timezone_id`).
- Removed: the `queue` bundle key, `health` rule names, `For each` concurrency and continuous-job claims (not in the fetched pages).

Method: documentation only; no commands were run.
