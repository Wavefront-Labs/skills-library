---
id: computing-software.data-engineering.prefect.runtime-context-access
name: runtime-context-access
category: computing-software
field: data-engineering
product: prefect
tags: [runtime, flow-run, get-run-context, deployment, mocking]
level: practitioner
status: docs-checked
description: "Read deployment, flow run and task run details through prefect.runtime, mock values with environment variables and use run context objects."
sources:
  - https://docs.prefect.io/v3/concepts/runtime-context
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read information about the current run from inside code.

`prefect.runtime` has three submodules: `deployment`, `flow_run` and `task_run`. Unavailable values return an empty value; for example `runtime.deployment.name` is `None` outside a deployment.

```python
from prefect import flow, task, runtime

@task
def t(y):
    print(runtime.task_run.name, runtime.flow_run.parameters)

@flow(log_prints=True)
def f(x):
    print(runtime.flow_run.name, runtime.deployment.name)
    t(2)
```

Mocking for tests: environment variable `PREFECT__RUNTIME__{SUBMODULE}__{KEY_NAME}=value`, for example `export PREFECT__RUNTIME__TASK_RUN__FAKE_KEY='foo'` makes `task_run.fake_key` return `"foo"`. Values for existing attributes are cast to the attribute type; supported casts are `bool`, `int`, `float`, `str`, `datetime.datetime`. For list or dict values use `monkeypatch` or similar.

Run context objects (`prefect.context`):
- `get_run_context()` returns the current context and raises outside a flow or task run; a task run context wins if both exist.
- `FlowRunContext.get()` and `TaskRunContext.get()` return `None` instead of raising, so a task can read the flow run context.
- The flow run context is not sent to distributed task workers because it is costly to serialize.

## Checked
2026-11-08. Confirmed against the Prefect runtime context page: the three prefect.runtime submodules, empty value when unavailable, the PREFECT__RUNTIME__{SUBMODULE}__{KEY_NAME} mock schema and its cast types, get_run_context() behaviour, FlowRunContext.get() and TaskRunContext.get() returning None, and the flow run context not being sent to distributed task workers. Nothing removed.
Method: documentation only; no commands were run.
