---
id: computing-software.software-engineering.pydantic.pydantic-field-defaults-and-factories
name: pydantic-field-defaults-and-factories
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-defaults, default-factory, validate-default, mutable-default, field, required-field]
level: practitioner
status: docs-checked
description: "Set Pydantic field defaults: default, default_factory (including one taking validated data), validate_default and mutable defaults."
sources:
  - https://docs.pydantic.dev/latest/concepts/fields/
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give fields defaults correctly.

`Field()` assigned to an annotated attribute does not make the field optional: `name: str = Field(frozen=True)` is still required. The ellipsis form `Field(..., frozen=True)` makes that explicit but is discouraged because it does not play well with static type checkers.

Defaults:

```python
class User(BaseModel):
    name: str = 'John Doe'
    age: int = Field(default=20)
```

default_factory: a callable invoked per instance.

```python
class User(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
```

Since v2.10 the factory may take a single required argument; it receives the already validated data as a dict:

```python
class User(BaseModel):
    email: EmailStr
    username: str = Field(default_factory=lambda data: data['email'])
```
`data` only holds fields defined before this one (model field order); the example would fail if `username` were defined before `email`. Private attribute factories get the same ability since v2.13.

validate_default: defaults are not validated unless you ask, via the field parameter or the `validate_default` config value:

```python
class User(BaseModel):
    age: int = Field(default='twelve', validate_default=True)
User()  # ValidationError: Input should be a valid integer ... [type=int_parsing]
```

Mutable defaults: unlike `dataclasses` (which raises), Pydantic does not require a factory. If the default is not hashable, Pydantic deep-copies it for each instance:

```python
class Model(BaseModel):
    item_counts: list[dict[str, int]] = [{}]

m1 = Model(); m1.item_counts[0]['a'] = 1
Model().item_counts   #> [{}]
```

Type-checker note: static checkers use `default`, `default_factory` and `alias` from `Field()` to synthesize `__init__`, but they do not understand the `Annotated` form, so use the assignment form for these.

## Checked

Checked 2026-11-07. Re-read concepts/fields and concepts/models in full (in chunks) and compared every claim; no changes needed.

Method: documentation only; no commands were run.
