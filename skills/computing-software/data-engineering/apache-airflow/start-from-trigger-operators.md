---
id: computing-software.data-engineering.apache-airflow.start-from-trigger-operators
name: start-from-trigger-operators
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, start-from-trigger, deferrable-operators, starttriggerargs, worker-slots]
level: sme
status: docs-checked
description: "Make Airflow operators begin directly in the triggerer with start_from_trigger and StartTriggerArgs, skipping a worker slot, and know its templating and mapping limits."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/deferring.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Starting execution from the triggerer (start_from_trigger)

**Goal:** for pure-wait operators (sensors that only poll an async API) skip the worker entirely: the scheduler hands the TI straight to the triggerer (2.10+).

## Pattern
```python
from datetime import timedelta
from airflow.triggers.base import StartTriggerArgs
from airflow.sdk import BaseOperator

class WaitForJobOperator(BaseOperator):
    start_trigger_args = StartTriggerArgs(
        trigger_cls="company.triggers.JobDoneTrigger",
        trigger_kwargs={"poll_interval": 60},
        next_method="execute_complete",
        next_kwargs=None,
        timeout=timedelta(hours=2),
    )
    start_from_trigger = True

    def __init__(self, job_id, **kw):
        super().__init__(**kw)
        self.job_id = job_id
        self.start_trigger_args.trigger_kwargs = {"job_id": job_id, "poll_interval": 60}

    def execute_complete(self, context, event):
        if event["status"] != "success":
            raise RuntimeError(event)
        return event["job_id"]
```
The task is deferred straight to the triggerer without going into a worker. After the trigger finishes, the task may be sent back to a worker to run `next_method` (`execute_complete` here), or it can end directly with `end_from_trigger`.

## Limits
- All `trigger_kwargs` must be serializable by Airflow; the docs call this the main limitation of the feature.
- `start_from_trigger` and `trigger_kwargs` can also be set at the instance level in `__init__`.
- Mapped tasks get limited support: for a task with `start_from_trigger` set, the whole `__init__` is skipped, and the scheduler uses `start_from_trigger` and `trigger_kwargs` passed through `partial()` and `expand()` (with a fallback to the class attributes). Define `start_from_trigger` and `trigger_kwargs` as `__init__` parameters with exactly those names to enable it.
- If the task is sent back to a worker, the `__init__` arguments still take effect before `next_method`, but they do not affect the trigger.

## When it pays off
Pure waits where occupying a worker, even briefly, is wasted work, because the task goes to the triggerer without starting on a worker.

## Verify
The task instance reaches `deferred` without a worker running it first.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the `start_from_trigger` attribute and `StartTriggerArgs` fields (`trigger_cls`, `trigger_kwargs`, `next_method`, `next_kwargs`, `timeout`) with the 2.10.0 version note, the serializability limitation, instance-level overrides, the mapped-task behaviour and `end_from_trigger` (deferring.rst), and the `airflow.triggers.base` import. Removed the templating, `execute()` and executor-support claims and the worker start-up cost claims, which are not documented.

Method: documentation only; no commands were run.
