---
id: computing-software.data-engineering.apache-airflow.sensor-decorator-and-python-sensors
name: sensor-decorator-and-python-sensors
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, sensors, task-sensor-decorator, pythonsensor, sqlsensor, httpsensor, pokereturnvalue, reschedule-mode]
level: practitioner
status: docs-checked
description: "Write custom wait conditions in Airflow with @task.sensor (PokeReturnValue), SqlSensor and HttpSensor, choosing poke interval, mode and timeout to avoid hogging worker slots."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/sensors.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/sensor.py
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/deferring.rst
  - https://github.com/apache/airflow/blob/main/providers/common/sql/src/airflow/providers/common/sql/sensors/sql.py
  - https://github.com/apache/airflow/blob/main/providers/http/src/airflow/providers/http/sensors/http.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @task.sensor and Python/SQL/HTTP sensors

**Goal:** wait for a business condition (rows landed, API job finished) with a few lines of code, without occupying a worker slot for hours.

## @task.sensor with a return value
```python
from airflow.sdk import task, PokeReturnValue

@task.sensor(poke_interval=300, timeout=6 * 3600, mode="reschedule", soft_fail=False)
def export_ready(job_id: str) -> PokeReturnValue:
    status = vendor_api.get_job(job_id)
    if status["state"] == "FAILED":
        raise RuntimeError(f"vendor job failed: {status}")   # fail fast, do not wait for timeout
    return PokeReturnValue(is_done=status["state"] == "DONE", xcom_value=status.get("file_url"))

url = export_ready(job_id="{{ ti.xcom_pull('start_export') }}")
download(url)
```
Returning a bool also works; `PokeReturnValue` lets the sensor pass data downstream when done.

## SqlSensor
```python
from airflow.providers.common.sql.sensors.sql import SqlSensor
SqlSensor(
    task_id="partition_loaded",
    conn_id="warehouse",
    sql="select count(*) from raw.orders where load_date = '{{ ds }}'",
    success=lambda v: v > 0,          # first cell of first row
    poke_interval=600, timeout=4 * 3600, mode="reschedule",
)
```

## HttpSensor
```python
from airflow.providers.http.sensors.http import HttpSensor
HttpSensor(task_id="api_up", http_conn_id="partner_api", endpoint="health",
           response_check=lambda r: r.json().get("status") == "ok",
           poke_interval=60, timeout=1800, mode="reschedule")
```

## Mode choice
- `poke` (default): holds a worker slot (and a pool slot) for the whole runtime. Use it for short waits or short poke intervals.
- `reschedule`: frees the worker slot between pokes and is rescheduled later. Use it for long waits, with a poke interval above one minute.
- Deferrable sensors (`deferrable=True` on providers that support it) are cheaper still: the triggerer waits asynchronously.

## Timeouts
- `timeout`: time from the first poke, including reschedule delays, before the sensor fails (or is skipped with `soft_fail=True`); the default comes from `[sensors] default_timeout` (7 days).
- `execution_timeout` (from `BaseOperator`) checks only the running time, leaving out reschedule delays; in poke mode the two are equivalent.
- `exponential_backoff=True` grows the interval between pokes; cap it with `max_wait`.

## Gotchas
- A sensor that swallows errors and returns False waits until timeout on a hard failure. Raise on terminal states.
- In reschedule mode the poke interval should be more than one minute to avoid load on the scheduler; use poke or a deferrable sensor for shorter intervals.
- In poke mode each sensor holds a worker slot and a pool slot, so many concurrent sensors can exhaust them; consider a dedicated pool.

## Verify
- [ ] A terminal failure in the external system fails the sensor immediately.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `@task.sensor` and `PokeReturnValue(is_done, xcom_value)` (SDK exports and sensor source, `op_args`/`op_kwargs` templated), `SqlSensor` `success` callable on the first cell, `HttpSensor` `http_conn_id`, `endpoint`, `response_check` and `deferrable`, poke versus reschedule semantics, `timeout` versus `execution_timeout`, `exponential_backoff` with `max_wait`, and the 7 day default timeout. Removed the Airflow 2.x import note, the `up_for_reschedule` state claim and the under-one-minute poke guidance, which the docs do not state in that form.

Method: documentation only; no commands were run.
