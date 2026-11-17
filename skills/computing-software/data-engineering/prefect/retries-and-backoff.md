---
id: computing-software.data-engineering.prefect.retries-and-backoff
name: retries-and-backoff
category: computing-software
field: data-engineering
product: prefect
tags: [retries, retry-delay, jitter, backoff, retry-condition]
level: practitioner
status: docs-checked
description: "Configure Prefect flow and task retries: retry_delay_seconds lists, exponential_backoff, retry_jitter_factor, retry_condition_fn and global defaults."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/retries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make flows and tasks retry safely.

- `retries` (integer) on `@flow` or `@task`. A flow retries if it raises or returns a `Failed` state, such as a failed task state or future.
- Put `retries` on individual tasks so only that task reruns.
- `retry_delay_seconds`: an int, a list of ints (one delay per retry), or `exponential_backoff(backoff_factor=...)` from `prefect.tasks`.
- `retry_jitter_factor`: adds random time to delays so tasks do not retry in lockstep against an external system.
- `retry_condition_fn`: callable `(task, task_run, state)` returning a bool; `True` retries, `False` ends the task with its exception. Use it to skip retries for certain errors, such as particular HTTP status codes.

```python
from prefect import task
from prefect.tasks import exponential_backoff

@task(retries=4, retry_delay_seconds=exponential_backoff(backoff_factor=10),
      retry_jitter_factor=1)
def call_api(): ...
```

Nested flows: a parent retry reuses a completed child result only if the child sets `persist_result=True`. Otherwise it starts a new child run with its own retry budget and a new flow-run ID, so caches keyed on flow-run ID do not carry over.

Global defaults:

```bash
prefect config set PREFECT_TASKS_DEFAULT_RETRIES=2 PREFECT_TASKS_DEFAULT_RETRY_DELAY_SECONDS=30
```

Per-task `retries` and `retry_delay_seconds` override these defaults.

## Checked
2026-11-08. Confirmed against the retries how-to: retries and the Failed-state rule, per-task retries, retry_delay_seconds as int or list, exponential_backoff from prefect.tasks, retry_condition_fn signature and True/False meaning, retry_jitter_factor, nested flow persist_result behaviour and the PREFECT_TASKS_DEFAULT_RETRIES and PREFECT_TASKS_DEFAULT_RETRY_DELAY_SECONDS settings (the page example sets the delay to 1,10,100; the value 30 in this skill is only an example). Nothing removed.
Method: documentation only; no commands were run.
