---
id: computing-software.data-engineering.dbt.dbt-cloud-deploy-jobs
name: dbt-cloud-deploy-jobs
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-deployment, dbt-cloud-jobs, deploy-jobs, job-chaining, run-steps, dbt-cloud-api, environments]
level: practitioner
status: docs-checked
description: "Set up dbt Cloud deploy jobs: environments, commands and run steps, schedules vs job completion triggers, source freshness steps, run timeouts, and triggering via the API."
sources:
  - https://docs.getdbt.com/docs/deploy/deploy-jobs
  - https://docs.getdbt.com/docs/deploy/job-scheduler
  - https://docs.getdbt.com/docs/deploy/job-commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt Cloud deploy jobs

**Goal:** production dbt runs in dbt Cloud that are ordered, observable and cheap, with clear ownership.

## Environment first
- A deployment environment (see deploy-environments docs) is required before creating a deploy job; define environment variables for the job (for example `DBT_ENV_SECRET_` prefixed secrets).

## Job definition
- **Commands** (by default `dbt build`) run in order; add more with **Add command**:
```
dbt source freshness              # optional; can be a checkbox "Run source freshness"
dbt build --exclude tag:hourly
dbt run-operation refresh_bi_extracts
```
- The "Generate docs on run" and "Run source freshness" checkboxes add steps; if such a step fails the job can still succeed when later steps pass.
- Other job settings include environment variables, run timeout (cancel the run after the timeout) and "Compare changes against" deferral.

## Triggers
- **Schedule:** specific days with intervals or specific hours, or a cron schedule; all times are UTC with no daylight-saving adjustment.
- **Run when another job finishes:** run when an upstream deploy job (possibly in another project) completes with the selected statuses; this chains jobs. Needs the Starter or an Enterprise-tier plan.
- **API or manual triggers** also enqueue runs; see the dbt platform Administrative API reference for the exact endpoints and fields.
Runs queue until a run slot is free and any earlier run of the same job has finished (runs of one job execute serially).

## Job design
- One "main" job running `dbt build` on the whole DAG is the simplest start (the default command of a new deploy job is `dbt build`); split by cadence with tags only when needed.
- A `state:modified` selector on a scheduled job can finish successfully with zero models built when nothing changed since the last deferred run.
- Concurrency: the scheduler runs distinct runs of the same job serially; run slots limit how many jobs run at once.



## Gotchas
- Job runs are triggered in UTC; check the time zone of any cron schedule.
- You must have permissions on the project and job to configure a completion trigger.

## Verify
- [ ] Production job history shows the expected cadence and durations.
- [ ] The downstream job runs only after the upstream job finishes with the selected status.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt deploy jobs and job scheduler pages: default `dbt build` command, generate-docs and source-freshness checkboxes and their failure behaviour, run timeout, deferral option, schedule by days/intervals/specific hours or cron in UTC, trigger on job completion (plan availability, chaining, permissions), scheduler queue rules (serial runs of one job, run slots), `state:modified` on scheduled jobs. Removed the Administrative API request details, status codes, Airflow operator, notification and environment-version claims because they are not in the docs repository.

Method: documentation only; no commands were run.
