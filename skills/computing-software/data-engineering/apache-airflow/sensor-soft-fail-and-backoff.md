---
id: computing-software.data-engineering.apache-airflow.sensor-soft-fail-and-backoff
name: sensor-soft-fail-and-backoff
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, sensors, soft-fail, exponential-backoff, silent-fail, sensor-timeout, max-wait, never-fail]
level: practitioner
status: docs-checked
description: "Control how Airflow sensors give up: soft_fail to skip instead of fail, silent_fail/never_fail for flaky checks, and exponential_backoff with max_wait to reduce load."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/sensors.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/sensor.py
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sensor soft_fail, silent_fail and backoff

**Goal:** sensors that end the right way (skip, fail, or keep trying) and do not hammer the system they poll.

## Outcomes when the condition never arrives
| Setting | After `timeout` |
|---|---|
| default | task `failed` (retries apply) |
| `soft_fail=True` | task `skipped`; downstream skipped per trigger rules |

Use `soft_fail` when absence of data is a normal outcome (optional vendor file, holiday). Combine with a downstream `trigger_rule="all_done"` notifier if someone should know.

## Errors during a poke
| Setting | Exception raised inside `poke()` |
|---|---|
| default | task fails (retries apply) |
| `silent_fail=True` | exception logged, poke treated as "not yet", keeps sensing (not for `AirflowSensorTimeout`, `AirflowTaskTimeout`, `AirflowSkipException` or `AirflowFailException`) |
| `never_fail=True` (mutually exclusive with `soft_fail`) | an exception raised by the poke skips the sensor |

`silent_fail` suits flaky endpoints where the next poke is likely to work. Do not use it to hide real errors: a persistent error keeps being logged and retried until the timeout.

## Backoff
```python
from datetime import timedelta
S3KeySensor(
    task_id="wait_for_file",
    bucket_key="s3://landing/{{ ds }}/done.flag",
    poke_interval=60,
    exponential_backoff=True,           # growing intervals between pokes
    max_wait=timedelta(minutes=30),     # cap per-interval wait
    timeout=timedelta(hours=8).total_seconds(),
    mode="reschedule",
    soft_fail=True,
)
```
The interval grows exponentially from `poke_interval` with a hash-based jitter (so sensors do not poke simultaneously), and is capped by `max_wait` and the time left before `timeout`. Good for long waits where early arrival is unlikely.

## Retries interplay
When a poke raises an exception (and `silent_fail`, `soft_fail` and `never_fail` do not apply), the sensor task fails and can be retried according to `retries`. `timeout` is measured from the first poke. Consider `retries=0` on sensors, or handle transient errors with `silent_fail`.

## Gotchas
- `soft_fail` skips the sensor on timeout and when a poke raises `AirflowSensorTimeout`, `AirflowTaskTimeout` or `AirflowFailException`; other exceptions still fail the task.
- Skipped sensors propagate skips through `all_success` downstream: the whole rest of the run may silently skip.
- For a deferred sensor, a deferral timeout is converted to `AirflowSensorTimeout`, and `soft_fail` or `never_fail` then turn it into a skip.
- The default `timeout` is 7 days (`[sensors] default_timeout`).

## Verify
- [ ] Test DAG run with missing file ends `skipped` (soft_fail) and the notifier runs.
- [ ] Task logs show the growing intervals (`new reschedule interval is ...`).

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `BaseSensorOperator` source in the Task SDK: timeout and `soft_fail` skip semantics, which exceptions `silent_fail` and `soft_fail` handle, `never_fail` and its mutual exclusion with `soft_fail` (raises `ValueError`), exponential backoff with jitter capped by `max_wait` and the remaining timeout, deferral timeout handling, and the 7 day `default_timeout`. Removed the version gates, the 32 hour retry arithmetic and the provider-version claim, which are not documented.

Method: documentation only; no commands were run.
