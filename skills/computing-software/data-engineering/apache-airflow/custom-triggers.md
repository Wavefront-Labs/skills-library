---
id: computing-software.data-engineering.apache-airflow.custom-triggers
name: custom-triggers
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, custom-trigger, basetrigger, triggerer, deferrable-operators, triggerevent, asyncio, serialize, defer]
level: sme
status: docs-checked
description: "Write a custom Airflow trigger and deferrable operator: BaseTrigger serialize/run with asyncio, self.defer and execute_complete, timeouts, and a healthy triggerer loop."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/deferring.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom triggers and deferrable operators

**Goal:** wait on an external job (API job, query, file) without holding a worker slot, when no provider ships a deferrable operator for it.

## The trigger (runs in the triggerer's asyncio loop)
```python
import asyncio, httpx
from airflow.triggers.base import BaseTrigger, TriggerEvent

class AcmeJobTrigger(BaseTrigger):
    def __init__(self, job_id: str, conn_id: str, poll_interval: float = 30.0):
        super().__init__()
        self.job_id, self.conn_id, self.poll_interval = job_id, conn_id, poll_interval

    def serialize(self):
        return ("acme_provider.triggers.AcmeJobTrigger",          # importable path
                {"job_id": self.job_id, "conn_id": self.conn_id, "poll_interval": self.poll_interval})

    async def run(self):
        token = await get_token_async(self.conn_id)                # async I/O only
        async with httpx.AsyncClient() as client:
            while True:
                r = await client.get(f"https://acme/jobs/{self.job_id}", headers={"Authorization": token})
                state = r.json()["state"]
                if state in ("SUCCEEDED", "FAILED"):
                    yield TriggerEvent({"state": state, "job_id": self.job_id})
                    return
                await asyncio.sleep(self.poll_interval)
```

## The operator
```python
from datetime import timedelta
from airflow.sdk import BaseOperator
class AcmeRunJobOperator(BaseOperator):
    def __init__(self, *, spec: dict, conn_id="acme_default", **kw):
        super().__init__(**kw); self.spec, self.conn_id = spec, conn_id

    def execute(self, context):
        job_id = start_job(self.conn_id, self.spec)                # sync call is fine here (worker)
        self.defer(trigger=AcmeJobTrigger(job_id, self.conn_id),
                   method_name="execute_complete", timeout=timedelta(hours=6))

    def execute_complete(self, context, event):
        if event["state"] != "SUCCEEDED":
            raise RuntimeError(f"job {event['job_id']} failed")
        return event["job_id"]
```

## Rules
- **`run()` must be asynchronous** and `await` whenever it does a blocking operation (use `asyncio.sleep`, not `time.sleep`). Code that blocks stalls the whole triggerer process; Airflow tries to detect it and warns in the triggerer logs, and `PYTHONASYNCIODEBUG=1` adds extra checks while developing. Filesystem calls on network-backed storage can block too.
- `run()` must `yield` its `TriggerEvent`s, not return them; returning before yielding at least one event, or raising, fails the waiting task instances.
- `__init__` and `serialize()` are a pair: the trigger is serialized and re-instantiated on whichever triggerer runs it, so take everything from `__init__` and avoid persistent state.
- Assume a trigger can run more than once (for example after a network partition) and avoid side effects such as inserting database rows; Airflow de-duplicates events fired in several places.
- `cleanup` always runs after `run` exits; implement `on_kill` to cancel external work when a user kills the task.
- `timeout` on `defer` is optional and defaults to no timeout; set it so hung external jobs fail the task.
- Restart the triggerer after changing a trigger, and keep trigger code off a DAG bundle (the triggerer does not initialize bundles).
- Operators can also start deferred directly with `start_from_trigger` (2.10+; see the start-from-trigger skill).

## Operate
Run multiple triggerers (`airflow triggerer`) on multiple hosts for HA; they coordinate with locking. Each has a default capacity of 1000 triggers (`[triggerer] capacity` or `--capacity`); triggers beyond total capacity are delayed. If a triggerer dies or is partitioned, Airflow reschedules its triggers elsewhere after waiting 2.1 times `triggerer.job_heartbeat_sec`. Watch the triggerer logs for blocking-code warnings.

## Verify
- [ ] Task shows state `deferred` while the job runs and no worker slot is used.
- [ ] Killing the triggerer mid-wait: another triggerer resumes the trigger and the task completes.
- [ ] No blocking-code warnings in the triggerer logs.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the trigger design constraints (`serialize`/`__init__` pairing, asynchronous `run` that yields events, run-more-than-once, `cleanup` and `on_kill`, restart on change, no DAG bundle), `self.defer(trigger, method_name, kwargs, timeout)` with timeout defaulting to none, `execute_complete(context, event)`, `airflow.sdk.BaseOperator`, HA triggerers, capacity 1000 (also in config.yml) and the 2.1 times job heartbeat rescheduling (deferring.rst). Removed the `AirflowException` import, the `sync_to_async` advice, the `blocked_main_thread` metric name and the quoted warning text, which are not documented.

Method: documentation only; no commands were run.
