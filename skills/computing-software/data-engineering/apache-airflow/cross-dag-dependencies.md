---
id: computing-software.data-engineering.apache-airflow.cross-dag-dependencies
name: cross-dag-dependencies
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, externaltasksensor, triggerdagrunoperator, cross-dag-dependencies, execution-delta, external-task-marker, wait-for-completion, dag-dependencies]
level: practitioner
status: docs-checked
description: "Wire Airflow DAG-to-DAG dependencies: assets vs ExternalTaskSensor vs TriggerDagRunOperator, aligning logical dates, deferrable waits, and clearing across DAGs."
sources:
  - https://github.com/apache/airflow/blob/main/providers/standard/docs/sensors/external_task_sensor.rst
  - https://github.com/apache/airflow/blob/main/providers/standard/src/airflow/providers/standard/sensors/external_task.py
  - https://github.com/apache/airflow/blob/main/providers/standard/src/airflow/providers/standard/operators/trigger_dagrun.py
  - https://github.com/apache/airflow/blob/main/providers/standard/docs/operators/trigger_dag_run.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-DAG dependencies

**Goal:** DAG B runs after DAG A's relevant work, reliably, with the right date alignment.

## Choose the mechanism
| Mechanism | Coupling | Use when |
|---|---|---|
| **Assets** (data-aware scheduling) | Loose: B depends on data, not on A | Default choice when B follows A's data |
| `TriggerDagRunOperator` in A | A knows about B (push) | A orchestrates a sequence; pass conf |
| `ExternalTaskSensor` in B | B knows about A's task (pull) | Both on time schedules, B waits for A's same-period run |

## ExternalTaskSensor
```python
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
from datetime import timedelta
wait = ExternalTaskSensor(
    task_id="wait_for_orders_load",
    external_dag_id="load_orders",
    external_task_id="publish",              # or None to wait for the whole DAG run
    allowed_states=["success"],
    failed_states=["failed", "upstream_failed"],   # fail fast instead of waiting forever
    execution_delta=timedelta(hours=1),      # A runs at 01:00, B at 02:00 -> look 1h back
    timeout=3 * 3600,
    deferrable=True,                         # waits in the triggerer instead of a worker
)
```
- By default the sensor looks at the same logical date as its own run; `execution_delta` (a positive `timedelta`) looks back, and `execution_date_fn` handles complex mappings (pass only one of the two). With mismatched schedules it waits for a run that never exists, until timeout.
- `failed_states` defaults to `None`: by default the sensor does not fail when the external task fails; it keeps checking until it times out. Set `failed_states` to fail fast. `skipped_states` can make it skip.
- `external_task_id` and `external_task_group_id` cannot both be set; with neither, the sensor waits for the whole DAG run. `check_existence=True` stops waiting if the external DAG or task does not exist.
- `ExternalTaskMarker` in A makes clearing A's task also clear B's task for the matching date, but only if "Recursive" is selected when clearing.

## TriggerDagRunOperator
```python
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
trigger = TriggerDagRunOperator(
    task_id="trigger_mart",
    trigger_dag_id="build_orders_mart",
    conf={"source_run": "{{ run_id }}"},
    logical_date="{{ logical_date }}",       # align dates if B uses them
    wait_for_completion=True, deferrable=True, poke_interval=60,
    reset_dag_run=True,                      # if a run exists for that date, clear it to rerun instead of raising
)
```
B reads `dag_run.conf`. Set B's `schedule=None` so it runs only when triggered. With `wait_for_completion=True` the defaults are success for `allowed_states` and `failed` for `failed_states`.

## Gotchas
- Sensors in `poke` mode hold a worker slot the whole time: use `mode="reschedule"` or `deferrable=True`.
- Renaming a DAG or task leaves sensors waiting for something that no longer exists: keep ids in shared constants.
- Without `reset_dag_run=True`, triggering a run that already exists raises `DagRunAlreadyExists`.

## Verify
- [ ] B waits only for A's matching period.
- [ ] Failed A makes B fail quickly, not time out after hours.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `ExternalTaskSensor` parameters and defaults (`allowed_states` success, `failed_states` None, `execution_delta`, `execution_date_fn`, `check_existence`, `deferrable`, mutually exclusive id arguments) and `ExternalTaskMarker` needing Recursive clearing (provider docs and sensor source), and `TriggerDagRunOperator` parameters (`conf`, `logical_date`, `wait_for_completion`, `poke_interval`, `reset_dag_run`, default states; operator source). Removed the version tags, the combined `reschedule` plus `deferrable` example and the Browse-menu view claim, which are not documented.

Method: documentation only; no commands were run.
