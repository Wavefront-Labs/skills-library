---
id: computing-software.data-engineering.apache-airflow.depends-on-past-and-wait-for-downstream
name: depends-on-past-and-wait-for-downstream
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, depends-on-past, wait-for-downstream, sequential-runs, max-active-runs, incremental-dependencies, stuck-runs]
level: practitioner
status: docs-checked
description: "Enforce run-to-run ordering in Airflow with depends_on_past, wait_for_downstream and max_active_runs, and unblock runs stuck waiting on a failed previous run."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/tasks.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# depends_on_past and wait_for_downstream

**Goal:** guarantee that today's incremental task does not run until yesterday's succeeded, when the logic is genuinely cumulative (running totals, SCD snapshots, append-only state).

## Settings
```python
@task(depends_on_past=True)
def update_running_balance(): ...

@task(depends_on_past=True, wait_for_downstream=True)
def extract_increment(): ...
```
- `depends_on_past=True`: task instance runs only if the **same task** in the previous DAG run succeeded or was skipped.
- `wait_for_downstream=True` (`depends_on_past` is forced to True): an instance of task X also waits for the tasks **immediately** downstream of the previous instance of X to succeed or be skipped; tasks further downstream are ignored. Useful when instances of X alter the same asset that downstream tasks read.
- DAG level `max_active_runs=1`: simpler, serialises whole runs. Often enough on its own.

## Behaviour details
- The very first automated run has no previous run to depend on, so the task still runs.
- `[core] ignore_first_depends_on_past_by_default` (default `True`) makes the first task instance of a task ignore `depends_on_past`, where "first" means no task instance in the database with an earlier logical date, so a newly added task needs no manual marking.
- The previous instance must be `success` or `skipped`; a failed one keeps the new instance from running until it is fixed.

## Unblocking
1. Fix and re-run the failed previous task instance (clear it).
2. Or mark it success if the data is known good or intentionally skipped.
3. The blocked instance can then run.

## When not to use it
- Idempotent partition overwrites (each run touches only its own interval): no need for ordering; parallel backfills are faster.
- Catch-up of many runs with `depends_on_past`: each run's task waits for the previous one, so backfill time is roughly the sum of the runtimes.

## Gotchas
- The docs ask you to pay special attention to `start_date`: the past dependency is not enforced only on the schedule of the task's `start_date`, and you should watch DAG run activity when introducing `depends_on_past=True`, unless you plan to backfill the new task.

## Verify
- [ ] Failing run N in staging keeps run N+1's task from running.
- [ ] Runbook documents how to unblock (clear vs mark success).

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `depends_on_past` semantics (previous instance success or skipped; first automated run still runs), `wait_for_downstream` and its forced `depends_on_past` and immediate-downstream-only scope (operator docstring), `[core] ignore_first_depends_on_past_by_default` default True (config.yml), and the start_date warning (dag-run and tasks docs). Removed the Airflow 2 backfill flag, the dependency-reason text, the REST unblocking note and the manual-run, catchup and mapped-index gotchas, which are not documented.

Method: documentation only; no commands were run.
