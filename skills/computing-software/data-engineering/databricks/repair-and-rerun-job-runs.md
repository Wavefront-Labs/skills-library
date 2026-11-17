---
id: computing-software.data-engineering.databricks.repair-and-rerun-job-runs
name: repair-and-rerun-job-runs
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, databricks-workflows, repair-run, rerun-failed-tasks, job-retries, incident-recovery, idempotency]
level: practitioner
status: docs-checked
description: "Recover failed Databricks job runs with repair run: rerun only failed tasks and dependents, override parameters, use the API/CLI, and make tasks safe to rerun."
sources:
  - https://docs.databricks.com/aws/en/jobs/repair-job-failures
  - https://docs.databricks.com/api/workspace/jobs/repairrun
  - https://docs.databricks.com/aws/en/jobs/configure-task#retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repair and rerun failed job runs

**Goal:** after a failure, rerun only what failed (and what depends on it), in the same run, without redoing hours of successful work.

## 1. What repair does
- Reruns selected tasks of an existing run; `rerun_dependent_tasks` also repairs the tasks that depend on them, even if they previously succeeded.
- The repair is part of the same run (same `run_id`, a new `repair_id`), so run history and task values stay together.

## 2. UI
Job run page > **Repair run**; the repair docs (jobs/repair-job-failures) describe the dialog.

## 3. API / CLI
```bash
databricks jobs repair-run <run-id> --rerun-all-failed-tasks
databricks jobs repair-run <run-id> --json '{"rerun_tasks": ["load_orders"], "rerun_dependent_tasks": true}'
```
A second repair of the same run must pass `latest_repair_id` (the ID of the latest repair, from the run's repair history) so repairs stay sequential.

## 4. Retries vs repair
| | Task retries | Repair |
|---|---|---|
| Trigger | automatic, inside the run | manual or scripted after the run ends |
| Use for | transient errors (spot loss, throttling) | fixed code/data, upstream outage over |
| Config | `max_retries`, `min_retry_interval_millis`, `retry_on_timeout` | none |
Set 1-3 retries on tasks talking to flaky external systems; don't retry deterministic failures (bad SQL), they just burn compute.

## 5. Make tasks repair-safe
- Idempotent writes: MERGE on keys or overwrite by run date, never blind `append` for batch tasks.
- Parameterise by logical date (a `run_date` job parameter) instead of `current_date()`, so a repair tomorrow processes yesterday's date.
- Avoid side effects that can't repeat (emails, external API posts) without dedup keys.

## Verify
- [ ] Repairing a failed run reprocesses only the failed branch (check task durations).
- [ ] Repaired tasks produce no duplicates (row counts before/after match expectations).
- [ ] Tasks use a run-date parameter, not wall-clock dates.

## Checked
2026-10-28. Confirmed against the Jobs API repair-run reference and the CLI jobs commands page (repair_id, latest_repair_id must be supplied on subsequent repairs, rerun_all_failed_tasks, rerun_dependent_tasks, --json) and the job task retries settings (max_retries, min_retry_interval_millis, retry_on_timeout). Removed: job_parameters in the repair body, job cluster recreation and current-definition claims, UI dialog detail, task value retention, streaming checkpoint claim, replaceWhere.
Method: documentation only; no commands were run.
