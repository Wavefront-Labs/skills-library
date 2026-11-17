---
id: computing-software.data-engineering.databricks.jobs-api-and-cli
name: jobs-api-and-cli
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-jobs, jobs-api, databricks-cli, run-now, runs-get, repair-run, automation]
level: practitioner
status: docs-checked
description: "Drive Databricks Jobs from scripts and external orchestrators with the Jobs API 2.2 and CLI: run-now with parameters, poll run state, fetch task output, cancel and repair runs."
sources:
  - https://docs.databricks.com/api/workspace/jobs
  - https://docs.databricks.com/en/dev-tools/cli/commands.html
  - https://docs.databricks.com/en/jobs/repair-job-failures.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jobs API and CLI

**Goal:** trigger and monitor Databricks jobs from Airflow, CI or other systems reliably, with parameters and proper failure reporting.

## Auth
Service principal with OAuth M2M (preferred) or PAT. Select credentials with `--profile <name>` or `DATABRICKS_CONFIG_PROFILE`; OAuth M2M needs the workspace host, client ID and client secret (see the OAuth M2M page).
Grant the SP `CAN MANAGE RUN` on the job.

## Trigger with parameters
```bash
databricks jobs run-now 123456 --json '{"job_parameters": {"run_date": "2026-10-17", "full_refresh": "false"}}' --profile prod-sp --no-wait
```
REST:
```bash
curl -s -X POST "$HOST/api/2.2/jobs/run-now" -H "Authorization: Bearer $TOKEN" \
  -d '{"job_id": 123456, "job_parameters": {"run_date": "2026-10-17"}, "idempotency_token": "load-2026-10-17"}'
```
`idempotency_token` guarantees at most one run per token (safe retries of the trigger call). Returns `run_id`.

## Poll
```bash
databricks jobs get-run $RUN_ID --profile prod-sp -o json | jq '.state, .status'
```
- `status.state`: `QUEUED`, `PENDING`, `RUNNING`, `TERMINATING`, `TERMINATED`, `BLOCKED`, `WAITING`.
- `status.termination_details.code`: `SUCCESS`, `RUN_EXECUTION_ERROR`, `CANCELED`, `USER_CANCELED`, `DRIVER_ERROR`, `CLUSTER_ERROR`, `INTERNAL_ERROR`, and others listed in the API reference.
- `--no-wait` makes the CLI not wait for the run to reach a terminal state; without it the CLI waits.

## Task output and errors
```bash
databricks jobs get-run $RUN_ID -o json | jq -r '.tasks[] | [.task_key, .run_id, .status.termination_details.code] | @tsv'
databricks jobs get-run-output $TASK_RUN_ID -o json | jq '.error, .error_trace, .notebook_output.result'
```
`get-run-output` works on **task** run ids. Notebook tasks can return a value via `dbutils.notebook.exit("...")`; the API returns only the first 5 MB of output, so return a small JSON status string, not data.

## Cancel, repair, list
```bash
databricks jobs cancel-run $RUN_ID
databricks jobs repair-run $RUN_ID --rerun-all-failed-tasks --latest-repair-id $REPAIR_ID
databricks jobs list-runs --job-id 123456 --active-only
```
`--rerun-all-failed-tasks` repairs all failed tasks; `--rerun-dependent-tasks` also repairs tasks that depend on the ones in `rerun_tasks`. Pass the latest repair ID on later repairs of the same run.

## Orchestrator integrations
Prefer triggering **jobs** (defined in Asset Bundles) over submitting one-off runs (`runs/submit`), so job config is versioned and visible.

## Gotchas
- Use `job_parameters` in run-now for jobs that define job parameters; the run-now API reference lists the other parameter fields.
- Poll at a modest interval (tens of seconds), not every second, to stay clear of API rate limits.
- `max_concurrent_runs` limits concurrent runs; the job's `queue.enabled` setting controls queueing of extra runs (API reference).

## Verify
- [ ] Trigger script retried twice with the same idempotency token creates one run.
- [ ] Failure path surfaces the failing task key and error trace in the caller's logs.

## Checked
2026-10-28. Confirmed against the Jobs API reference (run-now, repair, run state and termination values, idempotency_token, 5 MB get-run-output limit, queue.enabled), the CLI jobs commands page (--no-wait, --rerun-all-failed-tasks, --rerun-dependent-tasks, --latest-repair-id, --active-only, get-run-output) and the OAuth M2M page (profile selection, CAN MANAGE RUN on job parameters page). Removed: the .databrickscfg key names, the claim that 2.2 status replaces life_cycle_state, CLI exit-code behaviour, Airflow deferrable and Azure Data Factory remarks, the legacy notebook_params rejection claim and the queued-or-skipped behaviour.
Method: documentation only; no commands were run.
