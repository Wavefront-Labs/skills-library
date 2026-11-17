---
id: computing-software.data-engineering.prefect.task-invocation-and-futures
name: task-invocation-and-futures
category: computing-software
field: data-engineering
product: prefect
tags: [tasks, submit, delay, futures, quote, opaque]
level: practitioner
status: docs-checked
description: "Call Prefect tasks directly, with .submit or .delay, control future resolution with quote and opaque, and know how task keys and states behave."
sources:
  - https://docs.prefect.io/v3/concepts/tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the right way to invoke a task.

Declare with `@task` (for example `@task(log_prints=True)`).

Invocation:
- `task(...)`: runs and blocks until complete, returns the result.
- `task.submit(...)`: returns a `PrefectFuture` immediately; resolve with `.result()` or `.wait()` from the same context that submitted it.
- `task.delay(...)`: returns a `PrefectFuture` immediately and runs on a separate task worker; the caller need not resolve it from the submitting context. A delayed task starts in `Scheduled` before `Pending`.
- `wait_for`: parameter that adds explicit state dependencies.

A downstream task given an upstream future or result will not start until the upstream task is `Completed`.

Parameter annotations from `prefect.utilities.annotations`:

| Annotation | Resolves futures | Traverses contents |
| - | - | - |
| none | yes | yes |
| `quote` | no | no |
| `opaque` | yes | no |

```python
from prefect.utilities.annotations import opaque, quote
run_pipeline(quote(pipeline))
run_pipeline.submit(opaque(future))
```

Reconstruction: dataclasses and named tuples are rebuilt with `dataclasses.replace()` (re-running `__init__` and `__post_init__`); Pydantic models with `model_construct()` (skipping validators).

A task key is a hash of the task name and its fully qualified function name. Orchestration is client-side and task updates are batched, so UI and API task states are eventually consistent.

## Checked

2026-11-08. Direct, submit and delay invocation behaviour, the Scheduled-before-Pending state for delayed tasks, wait_for and implicit dependencies, the quote and opaque table, dataclass and Pydantic reconstruction, the task key definition and client-side batched updates confirmed against the Tasks page.

Method: documentation only; no commands were run.
