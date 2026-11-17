---
id: computing-software.software-engineering.pydantic.pydantic-create-model-dynamically
name: pydantic-create-model-dynamically
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-create-model, dynamic-models, namespace, base, private-attr, runtime]
level: practitioner
status: docs-checked
description: "Create Pydantic models at runtime with create_model: field tuples, __base__, __config__, __namespace__, pickling and security note."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build a model when field definitions are only known at runtime.

```python
from pydantic import BaseModel, create_model

DynamicFoobarModel = create_model('DynamicFoobarModel', foo=str, bar=(int, 123))
# same as: class StaticFoobarModel(BaseModel): foo: str; bar: int = 123
```

Field definitions are keyword arguments, each either:
- a single element: the type annotation (since v2.11 any type; before, only an `Annotated` form), or
- a two-tuple `(type, value)` where value is a default or `Field()`.

Advanced:

```python
DynamicModel = create_model(
    'DynamicModel',
    foo=(str, Field(alias='FOO')),
    bar=Annotated[str, Field(description='Bar field')],
    _private=(int, PrivateAttr(default=1)),
)
```

Special keyword arguments:
- `__base__`: extend a base model, e.g. `create_model('BarModel', apple=(str, 'russet'), banana=(str, 'yellow'), __base__=FooModel)`; `BarModel.model_fields.keys()` is `['foo', 'bar', 'apple', 'banana']`.
- `__config__`: customize the model config.
- `__namespace__` (added v2.14): attach validators, methods or computed fields via the class namespace. Keys must not clash with field names. `__validators__` is removed in v3, use `__namespace__`.

```python
UserModel = create_model(
    'UserModel', first_name=str, last_name=str,
    __namespace__={
        'check_alphanum': field_validator('first_name', 'last_name')(alphanum),
        'full_name': computed_field(property(full_name)),
    },
)
```
Here `alphanum(cls, v)` asserts `v.isalnum()`, and `UserModel(first_name='J%hn', last_name='Doe')` fails with "Assertion failed, must be alphanumeric".

Pickling a dynamic model: define it globally and provide the `__module__` argument.

Warning: create_model may execute arbitrary code in field annotations if string references need evaluating (see the Python annotationlib security notes).

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
