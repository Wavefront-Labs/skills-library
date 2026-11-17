---
id: computing-software.devops-ci-cd.argo-workflows.cron-dst-and-stop-strategy
name: cron-dst-and-stop-strategy
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [cron-dst, stop-strategy, last-scheduled-time, cronworkflow-succeeded, daylight-saving]
level: advanced
status: docs-checked
description: "Handle daylight saving transitions in timezone cron schedules with a when expression and stop a CronWorkflow automatically with stopStrategy.expression."
sources: ["https://argo-workflows.readthedocs.io/en/latest/cron-workflows/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cron daylight saving and stopStrategy
With `timezone` set, daylight saving is honoured, so a schedule can run once, twice or not at all on transition days. When the clock jumps forward (US 2020-03-08), a `0 2 * * *` run is skipped that day. When it falls back (2020-11-01), a `59 1 * * *` run fires twice, once in PDT and once in PST.

Fix a skipped time with two schedules and a `when` guard that allows a run only if the last one was over an hour ago:

```yaml
schedules:
  - 30 2 * * *
  - 0 3 * * *
when: "{{= cronworkflow.lastScheduledTime == nil || (now() - cronworkflow.lastScheduledTime).Seconds() > 3600 }}"
```

The 03:00 run then only fires on the day 02:30 was skipped. Warning from the page: creating the CronWorkflow between the desired time and 03:00 makes it run at 03:00 because it has never run before.

For duplicate times use one schedule (`30 1 * * *`) with the same guard and a 7200 second threshold; the second 01:30 is suppressed.

Automatic stop uses `stopStrategy.expression` with the variables `cronworkflow.succeeded` and `cronworkflow.failed`, for example `cronworkflow.succeeded >= 1` or `cronworkflow.failed >= 3`. Prefer `>=` over `==`: a run already in flight when the condition is reached still completes, so an every-minute schedule with a 90 second Workflow stops after two completions.

## Checked
2026-11-03. Confirmed against the Argo Workflows Cron Workflows page (Daylight Saving and Automatically Stopping sections): DST behaviour and the 2020 examples, both `when` guards with 3600 and 7200 second thresholds, the never-run warning, `stopStrategy.expression` variables and the scheduling-versus-completions note. Nothing removed.
Method: documentation only; no commands were run.
