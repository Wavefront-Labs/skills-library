---
id: computing-software.data-engineering.prefect.flow-parameter-validation
name: flow-parameter-validation
category: computing-software
field: data-engineering
product: prefect
tags: [parameters, validate-parameters, pydantic, type-validation, flows]
level: intro
status: docs-checked
description: "Define Prefect flow inputs as typed parameters, rely on default type validation, disable it with validate_parameters=False, and use pydantic models."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/pass-inputs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pass validated inputs to a flow.

Workflow inputs are parameters of the `@flow` function; defaults work as in Python. Pass arguments in the call.

```python
from prefect import flow

@flow
def my_workflow(name: str = "World"):
    return f"Hello, {name}!"

my_workflow(name="Marvin")
```

Type validation is on by default. `my_workflow(name=1)` fails with a type validation error because the parameter is annotated `str`.

Disable it per flow:

```python
@flow(validate_parameters=False)
def my_workflow(name: str = "World"): ...
```

Pydantic: a parameter typed with a `pydantic` `BaseModel` subclass is coerced and validated, including when given a dict.

```python
from pydantic import BaseModel

class Model(BaseModel):
    a: int
    b: str

@flow
def flow_that_validates_parameters(model: Model): ...

flow_that_validates_parameters(model={"a": 1, "b": "fine"})
```

Use annotations on every parameter so validation has something to check. The guide does not state limits on parameter size or count.

## Checked
2026-11-08. Confirmed against the pass-inputs how-to: typed flow parameters, default type validation, validate_parameters=False and pydantic BaseModel coercion. The skill example uses a valid dict where the page uses an invalid one; the behaviour claim is the page's. Nothing removed.
Method: documentation only; no commands were run.
