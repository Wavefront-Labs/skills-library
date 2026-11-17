---
id: computing-software.data-engineering.apache-airflow.short-circuit-and-skipping-tasks
name: short-circuit-and-skipping-tasks
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, shortcircuitoperator, task-short-circuit, airflowskipexception, skipped-state, ignore-downstream-trigger-rules, conditional-execution]
level: practitioner
status: docs-checked
description: "Skip work conditionally in Airflow with @task.short_circuit, AirflowSkipException and trigger rules, controlling how skips propagate to downstream tasks."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dag-run.rst
  - https://github.com/apache/airflow/blob/main/providers/standard/src/airflow/providers/standard/operators/python.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-circuiting and skipping tasks

**Goal:** stop the rest of a run cleanly when there is nothing to do (no new files, holiday, upstream not ready) without marking it failed.

## @task.short_circuit
```python
@task.short_circuit(ignore_downstream_trigger_rules=True)
def has_new_files(prefix: str) -> bool:
    return len(list_keys(prefix)) > 0

check = has_new_files("landing/2026-10-17/")
check >> load() >> transform() >> publish()
```
- Falsy return -> all downstream tasks are set to `skipped`.
- `ignore_downstream_trigger_rules=True` (default): skips **every** downstream task regardless of their trigger rules.
- `ignore_downstream_trigger_rules=False`: skips only the direct downstream tasks; later tasks respect their own trigger rules (lets a final `notify` with `trigger_rule="none_failed"` still run).

## AirflowSkipException from any task
```python
from airflow.sdk.exceptions import AirflowSkipException

@task
def extract(ds=None):
    if is_holiday(ds):
        raise AirflowSkipException(f"{ds} is a holiday")
    ...
```
The task itself becomes `skipped`; downstream tasks with default `all_success` are skipped too (skip propagates through `all_success`).

## Trigger rules that interact with skips
| Rule | Runs when |
|---|---|
| `all_success` (default) | all upstream succeeded; any skip -> skipped |
| `none_failed` | no upstream failed (skips ok) |
| `none_failed_min_one_success` | no failures and at least one success: typical join after branching |
| `all_done` | all upstream finished, any state (cleanup, notifications) |
| `all_skipped` | every upstream skipped: "nothing to do" notifications |

## Run state
DAG run state comes from the leaf tasks: `success` if all leaves are `success` or `skipped`, `failed` if any leaf is `failed` or `upstream_failed`. A run with skipped tasks and no failures is therefore `success`.

## Choosing between branch and short-circuit
- Branch (`@task.branch`): choose **which** path runs.
- Short-circuit: decide **whether** the rest runs.

## Gotchas
- Returning a non-bool truthy object (e.g. a non-empty list) counts as True; return explicit bools.

## Verify
- [ ] Graph view after a no-data run: downstream tasks skipped, cleanup/notify tasks ran per their trigger rules.
- [ ] Tests cover both the True and the False path.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `ShortCircuitOperator` falsy/truthy semantics and both `ignore_downstream_trigger_rules` modes (docstring in the standard provider source), the trigger-rule definitions and leaf-based DAG run state. The `AirflowSkipException` class exists in `airflow.sdk.exceptions` (SDK source) and marks the task skipped (tasks.rst). Removed the soft_fail, clearing and empty-mapping gotchas and the dashboard advice, which were not confirmed in the docs.

Method: documentation only; no commands were run.
