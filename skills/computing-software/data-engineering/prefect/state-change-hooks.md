---
id: computing-software.data-engineering.prefect.state-change-hooks
name: state-change-hooks
category: computing-software
field: data-engineering
product: prefect
tags: [hooks, on-failure, on-completion, on-running, state-change]
level: practitioner
status: docs-checked
description: "Prefect state change hooks for flows and tasks: hook names, signatures, attaching methods, retry interaction and logging inside hooks."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/state-change-hooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run client-side code when a run changes state.

Hooks: `on_completion` (flow, task; enters `Completed`), `on_failure` (flow, task; `Failed`), `on_cancellation` (flow; `Cancelling`), `on_crashed` (flow; `Crashed`), `on_running` (flow, task; `Running`). `on_rollback` is a transaction hook, not a state change hook.

Signatures: flow hooks `hook(flow, flow_run, state)`; task hooks `hook(task, task_run, state)`.

Attach:
- decorator argument with a list: `@flow(on_failure=[fn])`, `@task(on_running=[fn])`
- decorator on the object: `@my_flow.on_failure` above the function
- per call: `my_task.with_options(on_failure=[fn])`

```python
def notify(flow, flow_run, state):
    print(f"{flow_run.name} -> {state.name}")

@flow(on_failure=[notify], on_completion=[notify])
def my_flow(): ...
```

Behaviour:
- With retries, `on_failure` fires only after retries are exhausted and the run is `Failed`.
- `on_running` runs synchronously before the task body, so slow hooks delay the task; it fires on every attempt (`retries=2` can fire it three times).
- Hooks run in the workflow process and execution is not guaranteed; use Automations for reliable responses.
- `get_run_logger()` raises `MissingContextError` in hooks; use `flow_run_logger(flow_run, flow)` or `task_run_logger` from `prefect.logging.loggers`.
- Extra kwargs: wrap the hook in `functools.partial`, pass it via `with_options`, and have the hook accept `**kwargs`.

## Checked
2026-11-08. Confirmed against the state change hooks how-to: the five hooks and which apply to flows and tasks, on_rollback being a transaction hook, hook arguments, decorator and with_options attachment, on_failure waiting for retries, on_running being synchronous and firing per attempt, client-side non-guaranteed execution, flow_run_logger for logging and the partial and kwargs pattern. Nothing removed.
Method: documentation only; no commands were run.
