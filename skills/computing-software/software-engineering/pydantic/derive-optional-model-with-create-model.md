---
id: computing-software.software-engineering.pydantic.derive-optional-model-with-create-model
name: derive-optional-model-with-create-model
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-dynamic-models, create-model, model-fields, fieldinfo-asdict, optional-fields, annotated]
level: advanced
status: docs-checked
description: "Derive a new Pydantic model from an existing one with create_model and FieldInfo.asdict(), making every field optional while keeping validators and constraints."
sources:
  - https://docs.pydantic.dev/latest/examples/dynamic_models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a variant of a model (every field optional; also usable to drop defaults or add aliases) with `create_model()`.

## Factory
```python
from typing import Annotated
from pydantic import BaseModel, Field, create_model

def make_fields_optional(model_cls: type[BaseModel]) -> type[BaseModel]:
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        f_dct = f_info.asdict()
        new_fields[f_name] = (
            Annotated[f_dct['annotation'] | None, *f_dct['metadata'], Field(**f_dct['attributes'])],
            None,
        )

    return create_model(
        f'{model_cls.__name__}Optional',
        __base__=model_cls,
        **new_fields,
    )
```
The star-unpacking inside `Annotated[...]` subscripts is for Python 3.11+; on Python 3.10 the page wraps the tuple: `Annotated[(f_dct['annotation'] | None, *f_dct['metadata'], Field(**f_dct['attributes']))]`.

- `__base__=model_cls` inherits validators, computed fields, etc.; the parent fields are overridden by the ones you define.
- The field tuple is `(annotation, default)`; the default here is `None`.

## What `asdict()` returns
For `f: Annotated[int, Field(gt=1), WithJsonSchema({'extra': 'data'}), Field(title='F')] = 1`:
- `annotation`: `int`
- `metadata`: `[Gt(1), WithJsonSchema({'extra': 'data'})]`
- `attributes`: `{'title': 'F'}`

The new annotation re-adds `None` (equivalent to `int | None`), unpacks the metadata, and rebuilds the remaining attributes through `Field(...)`.

## Use
```python
class Model(BaseModel):
    a: Annotated[int, Field(gt=1)]

ModelOptional = make_fields_optional(Model)
m = ModelOptional()
print(m.a)  # None
```

## Notes
- To preserve the input class for type hints use `ModelTypeT = TypeVar('ModelTypeT', bound=type[BaseModel])` (or `def make_fields_optional[ModelTypeT: type[BaseModel]](...)` on 3.12+). Static checkers still will not know all fields are optional.
- The `MISSING` sentinel can replace `None`: use it in both the annotation and the default.
- Copying and mutating original `FieldInfo` instances to reuse as `Annotated` metadata is not a supported pattern and could break or be deprecated at any point.

## Checked

Checked 2026-11-07. Compared every claim with the dynamic models example page (examples/dynamic_models.md): the `make_fields_optional` factory, the Python 3.10 tuple form versus 3.11+ star-unpacking, `__base__` inheriting validators and computed fields, the `asdict()` keys `annotation`, `metadata`, `attributes`, the `TypeVar` / PEP 695 notes, the `MISSING` alternative and the warning about copying `FieldInfo`. All confirmed; nothing removed.

Method: documentation only; no commands were run.
