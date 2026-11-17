---
id: computing-software.software-engineering.pydantic.pydantic-define-basic-model
name: pydantic-define-basic-model
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-basic-model, pydantic-data-conversion, basemodel, validation, model-dump, coercion]
level: practitioner
status: docs-checked
description: "Define a Pydantic BaseModel, instantiate it, read fields, dump it, and avoid the field-name versus type-name collision."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define a model with typed fields, validate input by instantiating it, and dump it back out.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
    model_config = ConfigDict(str_max_length=10)

user = User(id='123')
assert user.name == 'Jane Doe'
assert user.id == 123 and isinstance(user.id, int)
assert user.model_dump() == {'id': 123, 'name': 'Jane Doe'}
```

Rules from the docs:
- Models inherit from `BaseModel` and declare fields as annotated attributes. A field with a default is not required.
- Instantiation performs all parsing and validation. If no `ValidationError` is raised, the instance is valid.
- `model_fields_set` shows which field names were explicitly set at init (so you can tell a default from a provided value).
- Fields are plain attributes. Models are mutable by default, so `user.id = 321` works.
- `model_dump()` returns a dict, recursively. Calling `dict(user)` also gives a dict but nested fields are not recursively converted.
- Fields are validated in definition order, and that order is kept in JSON Schema, validation errors and serialization.

Useful members of every model class: `model_validate()`, `model_validate_json()`, `model_construct()`, `model_dump()`, `model_dump_json()`, `model_copy()`, `model_json_schema()`, `model_fields` (name to `FieldInfo`), `model_computed_fields`, `model_parametrized_name()`, `model_post_init()`, `model_rebuild()`. Instances add `model_extra` and `model_fields_set`.

Gotcha: do not name a field the same as its type. This fails validation because the annotated assignment is evaluated as `int: None = None`:

```python
class Boo(BaseModel):
    int: Optional[int] = None

Boo(int=123)  # will fail to validate
```

Model signature: `inspect.signature(Model)` is generated from the fields (keyword-only, for example `(*, id: int, name: str = None, description: str = 'Foo', pear: int) -> None`). A field's alias is preferred over its name when it is a valid identifier. A `**data` parameter is added if `extra` is `'allow'`.

Coercion: input may be cast to the field type and information can be lost (`Model(a=3.000, b='2.72', c=b'binary data')` dumps `{'a': 3, 'b': 2.72, 'c': 'binary data'}`); use strict mode for no conversion. Prefer concrete containers like `list[int]` over `Sequence` (a tuple input becomes a list; abstract types can validate slowly). Constructor arguments are often copied, so the validated list is not the same object as the input; model instances passed in are used as is unless `revalidate_instances='always'`.

Other model options the page covers: `ClassVar` attributes are not fields; `match` statements work with models (`case Pet(species='dog', name=dog_name)`) but only read attributes.

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
