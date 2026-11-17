---
id: computing-software.software-engineering.pydantic.pydantic-handle-extra-fields
name: pydantic-handle-extra-fields
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-extra-data, extra, model-config, pydantic-extra, forbid, allow, ignore]
level: practitioner
status: docs-checked
description: "Control unknown input keys on a Pydantic model with extra ignore, forbid or allow, and read them from __pydantic_extra__."
sources:
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide what happens to input keys that do not match a field.

Default: extra data does not error and is ignored.

```python
class Model(BaseModel):
    x: int

m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1}
```

Set `extra` in the model config:

```python
class Model(BaseModel):
    x: int
    model_config = ConfigDict(extra='allow')

m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.__pydantic_extra__ == {'y': 'a'}
```

The three values:
- `'ignore'`: extra data is ignored (the default).
- `'forbid'`: extra data is not permitted (validation fails).
- `'allow'`: extra data is stored in the `__pydantic_extra__` dict. You can annotate `__pydantic_extra__` explicitly to validate the extra fields.

Per-call override: the validation methods (for example `model_validate()`) accept an optional `extra` argument that overrides the model's `extra` setting for that call.

What counts as extra: any key not used to populate a field. That includes keys that match an alias of a field but lost to a higher-priority alias:

```python
class User(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str = Field(validation_alias=AliasChoices('first_name', 'fname'))

user = User.model_validate({'fname': 'J', 'first_name': 'John'})
# user.name == 'John'; user.__pydantic_extra__ == {'fname': 'J'}
```

Ordering: extra data is validated after all fields.

`model_construct()` behaviour with extras: with `'allow'` the extras are stored in `__pydantic_extra__` and in `__dict__`; with `'ignore'` they are dropped; with `'forbid'` no error is raised and the extra input is simply ignored.

Pydantic dataclasses also support extra data (configured through the dataclass config).

## Checked

Checked 2026-11-07. Re-read concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
