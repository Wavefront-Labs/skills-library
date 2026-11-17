---
id: computing-software.data-engineering.apache-airflow.branching-and-trigger-rules
name: branching-and-trigger-rules
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag, branching, trigger-rules, task-branch, branchpythonoperator, short-circuit, none-failed-min-one-success, all-done, skipped-tasks]
level: practitioner
status: docs-checked
description: "Control Airflow flow with branching and trigger rules: @task.branch, short_circuit, skip propagation, and picking the right trigger_rule for joins, cleanup and alert tasks."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dag-run.rst
  - https://github.com/apache/airflow/blob/main/providers/standard/src/airflow/providers/standard/operators/python.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branching and trigger rules

**Goal:** conditional paths in a DAG that skip correctly and rejoin without the join being skipped by accident.

## Branch
```python
from airflow.sdk import dag, task
from airflow.providers.standard.operators.empty import EmptyOperator

@dag(schedule="@daily", catchup=False)
def load_orders():
    @task.branch
    def choose(logical_date=None):
        return "full_load" if logical_date.day == 1 else "incremental_load"   # task_id or list of task_ids, or None to skip all downstream

    full = EmptyOperator(task_id="full_load")
    inc = EmptyOperator(task_id="incremental_load")
    join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")
    choose() >> [full, inc] >> join
load_orders()
```
Tasks downstream of the branch that were not chosen are **skipped**, and skips propagate: with the default `all_success`, `join` would be skipped too. Hence the trigger rule.

## Short-circuit
```python
@task.short_circuit
def has_new_files(): return len(list_new_files()) > 0
```
A falsy return skips downstream tasks. `ignore_downstream_trigger_rules=True` (the default) skips everything downstream regardless of trigger rules; with False only the direct downstream tasks are skipped and later tasks respect their own rules.

## Trigger rules
| Rule | Runs when | Typical use |
|---|---|---|
| `all_success` (default) | All upstream succeeded | Normal flow |
| `none_failed_min_one_success` | No upstream failed, at least one succeeded (skips ok) | Join after a branch |
| `none_failed` | No upstream failed/upstream_failed | Join where all branches could be skipped |
| `all_done` | All upstream finished, any state | Cleanup that must always run (prefer setup and teardown tasks) |
| `one_failed` | Any upstream failed | Alert / compensating task |
| `all_failed`, `one_success`, `one_done`, `all_skipped`, `none_skipped`, `all_done_min_one_success`, `all_done_setup_success` (the teardown default), `always` | Edge cases | |

## Gotchas
- A leaf task with `all_done` runs regardless of the other tasks' states, and if it succeeds the whole DAG run is marked `success` even if something failed earlier: DAG run state comes from the leaf tasks. Add a final "watcher" leaf task with `trigger_rule="one_failed"` that raises, or use teardown semantics.
- The returned task_id must reference a task **directly downstream** of the branch task.
- A task that is downstream of both the branch task and a selected task (such as a join) is not skipped.

## Verify
- [ ] `dag.test()` for both branch outcomes: the join runs in each.
- [ ] A forced failure in one path marks the DAG run failed.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `@task.branch` return contract (task id, list of ids, or None; direct downstream only), skip propagation with `all_success`, the full trigger-rule list and the `none_failed_min_one_success` join, `ignore_downstream_trigger_rules` default and False behaviour, and leaf-task based DAG run state with the `all_done` warning. Removed the Airflow 2.x import note, the 2.7 version gate and the task-group id return claim, which the docs do not state.

Method: documentation only; no commands were run.
