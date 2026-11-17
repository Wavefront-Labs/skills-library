---
id: computing-software.data-engineering.apache-airflow.dag-run-and-task-instance-states
name: dag-run-and-task-instance-states
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, dag-run-states, task-instance-states, clearing-tasks, mark-success]
level: practitioner
status: docs-checked
description: "Read and manipulate Airflow DAG run and task instance states: what each state means, how clear, mark success/failed and upstream_failed propagate, and CLI checks."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/tasks.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dag-run.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/cli/cli_config.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAG run and task instance states

**Goal:** know what a state means operationally and which action moves it where, so reruns do what you intend.

## DAG run states
`queued` -> `running` -> `success` | `failed`. The state is set from the leaf tasks: `success` if all leaves are `success` or `skipped`, `failed` if any leaf is `failed` or `upstream_failed` (a leaf with `all_done` that succeeds makes the run `success` even after earlier failures). A run whose `dagrun_timeout` expires is marked `failed` and its unfinished task instances `skipped`. `max_active_runs` (default from `[core] max_active_runs_per_dag`, 16) limits active runs per DAG.

## Task instance states
| State | Meaning | Typical action |
|---|---|---|
| none | not yet queued for execution (dependencies not met) | wait / check upstream |
| scheduled | dependencies met, it should run | check pool/concurrency |
| queued | assigned to an executor, awaiting a worker | check workers/queues |
| running | executing | logs |
| deferred | waiting in the triggerer | check triggerer |
| up_for_retry | failed, has retry attempts left and will be rescheduled | wait or clear |
| up_for_reschedule | a sensor in `reschedule` mode (or a retry policy that rescheduled it), will run again later | normal |
| success / failed | terminal | |
| skipped | branch/short-circuit/skip exception | |
| upstream_failed | an upstream failed and the trigger rule needed it | fix upstream then clear |
| removed | the task vanished from the DAG after the run started | ignore |

## Actions
- **Clear** resets task instances so they run again; the CLI offers `--upstream`, `--downstream`, `--only-failed` and `--only-running`.
- **Mark success/failed** sets state without running; use to unblock a run after a manual fix. Downstream tasks still need to run.
```bash
airflow tasks clear sales_daily -t "load_.*" -s 2026-10-01 -e 2026-10-07 --only-failed --downstream --yes
airflow dags list-runs sales_daily --state failed
airflow tasks states-for-dag-run sales_daily <run_id>
airflow dags state sales_daily <logical_date>
```

## Gotchas
- Clearing a task re-executes it with the same logical date/interval: only safe if the task is idempotent.
- A task instance that stays `queued` longer than `[scheduler] task_queued_timeout` (default 600 s) is retried or set to failed; that value also sets the lifetime of the workload JWT sent to the executor queue.
- A task instance can be stuck in `running` while its job is inactive (for example the worker ran out of memory); Airflow detects such formerly-called zombie tasks and handles them.

## Verify
After acting, the Grid view colours and `states-for-dag-run` output match the expected states.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the task instance state list and meanings (tasks.rst), leaf-based DAG run state with the `all_done` caveat and `dagrun_timeout` note (dag-run.rst), `[scheduler] task_queued_timeout` default 600 and `[core] max_active_runs_per_dag` default 16 (config.yml), and the CLI commands and flags (`tasks clear` with `-t -s -e --only-failed --downstream --yes`, `dags list-runs --state`, `tasks states-for-dag-run`, `dags state`) in the CLI source. Removed the clear-to-none and run-to-queued claims, recursive clearing, the upstream_failed clearing and mapped mark-success claims, which are not documented.

Method: documentation only; no commands were run.
