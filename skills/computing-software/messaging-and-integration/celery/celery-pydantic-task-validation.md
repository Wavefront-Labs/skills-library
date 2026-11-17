---
id: computing-software.messaging-and-integration.celery.celery-pydantic-task-validation
name: celery-pydantic-task-validation
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, celery-pydantic, pydantic, argument-validation, type-hints, model-dump, serialization, python]
level: practitioner
status: docs-checked
description: "Validate and convert Celery task arguments and return values with pydantic=True, including strict mode, context, dump kwargs, and cases where models must be sent as dicts."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use Pydantic models as task argument and return types (added in Celery 5.5.0).

```python
from pydantic import BaseModel

class ArgModel(BaseModel):
    value: int

class ReturnModel(BaseModel):
    value: str

@app.task(pydantic=True)
def x(arg: ArgModel) -> ReturnModel:
    assert isinstance(arg, ArgModel)
    return ReturnModel(value=f"example: {arg.value}")
```
Call with a model or a matching dict; the result comes back dumped via `BaseModel.model_dump()`:
```python
result = x.delay(ArgModel(value=1))   # or x.delay({'value': 1})
result.get(timeout=1)                 # {'value': 'example: 1'}
```
Validation covers only the task side. Since 5.7 models can be passed directly to `delay()` and `apply_async()`; the caller dumps with `pydantic_dump_kwargs` only if the worker would get back an equal model (checked with `==`), else the serializer raises `EncodeError`. Pass a dict instead for: models inside lists or dicts, `link`/`link_error` signatures, later chain tasks, chord bodies, `map()`/`starmap()`/`chunks()`, tasks called by name with `send_task()`, and models that would not round-trip (a `SecretStr` field, differing private attributes, subclass passed for a base-class annotation, a parameter not annotated as a model, or `pydantic_strict=True` with `datetime`/`UUID` fields).

## Limits
- Union types (`Union[A, B]`) and arguments to generics (`list[Model]`) are not supported; use `pydantic.RootModel` for lists.
- `Optional[ArgModel] = None` and `Optional[ReturnModel]` work; `x.delay()` returns `None`.
- A returned model is serialized only if it matches the annotation.

## Options
- `pydantic_strict`: default off; `True` enables strict validation.
- `pydantic_context`: extra validation context; already contains `celery_app` and `celery_task_name`.
- `pydantic_dump_kwargs`: extra `model_dump()` arguments; default only `mode='json'`. Add `by_alias=True` for aliased fields; add `exclude_unset=True` if the task uses `model_fields_set`.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
