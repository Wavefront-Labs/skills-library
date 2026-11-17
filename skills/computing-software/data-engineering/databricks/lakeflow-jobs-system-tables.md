---
id: computing-software.data-engineering.databricks.lakeflow-jobs-system-tables
name: lakeflow-jobs-system-tables
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, system-tables, lakeflow-system-tables, system-lakeflow, job-run-timeline, job-cost, job-reliability, observability]
level: practitioner
status: docs-checked
description: "Analyse Databricks job reliability, duration and cost across the workspace with system.lakeflow tables (jobs, job_run_timeline, job_task_run_timeline) joined to billing usage."
sources:
  - https://docs.databricks.com/aws/en/admin/system-tables/jobs
  - https://docs.databricks.com/aws/en/admin/system-tables/jobs-cost
  - https://docs.databricks.com/aws/en/admin/system-tables/pricing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job analytics with system.lakeflow tables

**Goal:** answer "which jobs fail most, which got slower, and which cost the most" with SQL instead of clicking through job pages.

## Tables
- `system.lakeflow.jobs`: job definitions (SCD-like; latest row per job_id = current name/owner/tags).
- `system.lakeflow.job_tasks`: task definitions.
- `system.lakeflow.job_run_timeline`: run start/end, `result_state`, `termination_code`, trigger type; long runs are split into hourly slices and `result_state` is populated only in the row that ends the run.
- `system.lakeflow.job_task_run_timeline`: per task run.
- `system.lakeflow.pipelines` and `system.lakeflow.pipeline_update_timeline` for pipelines.

## Failure rate by job (last 30 days)
```sql
with runs as (
  select workspace_id, job_id, run_id,
         max(result_state) as result_state,
         min(period_start_time) as start_time, max(period_end_time) as end_time
  from system.lakeflow.job_run_timeline
  where period_start_time >= current_date() - interval 30 days
  group by all
),
jobs as (
  select * from system.lakeflow.jobs
  qualify row_number() over (partition by workspace_id, job_id order by change_time desc) = 1
)
select j.name, count(*) runs,
       count_if(r.result_state in ('FAILED','ERROR','TIMED_OUT')) failed,
       round(100 * failed / runs, 1) fail_pct
from runs r join jobs j using (workspace_id, job_id)
group by all having runs >= 5 order by fail_pct desc limit 20;
```

## Duration trend (p50 / p90 per week)
```sql
select job_id, date_trunc('week', start_time) wk,
       percentile(timestampdiff(MINUTE, start_time, end_time), 0.5) p50_min,
       percentile(timestampdiff(MINUTE, start_time, end_time), 0.9) p90_min
from runs group by all order by job_id, wk;
```

## Cost per job
```sql
select u.usage_metadata.job_id as job_id, j.name,
       sum(u.usage_quantity * p.pricing.effective_list.default) as list_cost
from system.billing.usage u
join system.billing.list_prices p
  on u.cloud = p.cloud and u.sku_name = p.sku_name and u.usage_start_time >= p.price_start_time
 and (p.price_end_time is null or u.usage_start_time < p.price_end_time)
left join jobs j on j.job_id = u.usage_metadata.job_id and j.workspace_id = u.workspace_id
where u.usage_date >= current_date() - interval 30 days and u.usage_metadata.job_id is not null
group by all order by list_cost desc limit 20;
```
List prices, not discounted contract prices. Billing usage rows carry `usage_metadata.job_id` and `usage_metadata.job_run_id`.

## Practical uses
- Weekly reliability review: top failing jobs with owner from `jobs.creator_id` / `run_as`.
- Detect jobs with no successful run in N days (silent breakage).
- Spot jobs on all-purpose compute (billing SKU names containing `ALL_PURPOSE`) that should move to job compute.

## Gotchas
- Timelines are sliced per hour for long runs: aggregate per `run_id` first (as above).
- Records are typically available within one hour (longer for new workspaces); not a real-time alerting source.
- Jobs deleted long ago still appear in history; filter on `delete_time is null` in jobs when needed.

## Verify
- [ ] Dashboard/alert built on these queries shows the same failure count as the Jobs UI for a sample job.
- [ ] Cost query reconciles roughly with the account usage page for the period.

## Checked

2026-11-09. Confirmed on the Databricks jobs system tables, jobs cost and pricing pages: tables jobs, job_tasks, job_run_timeline, job_task_run_timeline, pipelines, pipeline_update_timeline; latest-row-per-job pattern with change_time and delete_time; creator_id and run_as columns; hourly slicing with result_state only on the final row; result states FAILED, ERROR, TIMED_OUT; availability within one hour; usage_metadata.job_id and job_run_id; list_prices price_start_time, price_end_time, sku_name, cloud and pricing.effective_list. Removed: the schema-enable step and serverless attribution wording (not on the pages read).

Method: documentation only; no commands were run.

