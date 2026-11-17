---
id: computing-software.software-engineering.pydantic.include-exclude-fields-on-dump
name: include-exclude-fields-on-dump
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-field-exclusion, exclude, include, exclude-unset, exclude-none, exclude-defaults, exclude-if, serialization]
level: practitioner
status: docs-checked
description: "Include or exclude fields when dumping Pydantic models: Field exclude and exclude_if, include/exclude params with nested keys, and exclude_unset/none/defaults."
sources:
  - https://docs.pydantic.dev/latest/concepts/serialization/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Include and exclude fields when serializing

Goal: drop or select fields at serialization time.

## At the field level

`Field(exclude=True)` always excludes; `Field(exclude_if=callable)` excludes when the callable returns true for the value.

```python
class Transaction(BaseModel):
    id: int
    private_id: int = Field(exclude=True)
    value: int = Field(ge=0, exclude_if=lambda v: v == 0)

Transaction(id=1, private_id=2, value=0).model_dump()   # {'id': 1}
```

Field-level exclusion takes priority over the `include` parameter.

## As serialization-method parameters

`exclude` removes the listed fields; `include` keeps only them. Both accept a set or a dict:

```python
t.model_dump(exclude={'user', 'value'})
t.model_dump(exclude={'user': {'username', 'password'}, 'value': True})
t.model_dump(include={'id': True, 'user': {'id'}})
```

- `False` to include inside `exclude` (or to exclude inside `include`) is not supported.
- Sequences and dicts accept item keys: `exclude={'hobbies': {-1: {'info'}}}` removes `info` from the last item; the equivalent `include` is `{'hobbies': {0: True, -1: {'name'}}}`.
- The key `'__all__'` applies to every member: `exclude={'hobbies': {'__all__': {'info'}}}`.

## By value

- `exclude_defaults`: drop fields equal (`==`) to their default.
- `exclude_none`: drop fields whose value is `None`.
- `exclude_unset`: drop fields not explicitly provided at instantiation. Pydantic tracks them in `model_fields_set`.

```python
class UserModel(BaseModel):
    name: str
    age: int = 18

user = UserModel(name='John')
user.model_fields_set                    # {'name'}
user.model_dump(exclude_unset=True)      # {'name': 'John'}
user.age = 21
user.model_dump(exclude_unset=True)      # {'name': 'John', 'age': 21}
```

Assigning to a field after creation removes it from the unset fields.

Tip from the page: the `MISSING` sentinel is an alternative to `exclude_unset`; any field whose value is `MISSING` is automatically excluded from output.

## Checked

Checked 2026-11-07. Compared every claim with the serialization concepts page (concepts/serialization.md): `Field(exclude=...)` and `exclude_if`, priority over `include`, set and dict forms of `include` / `exclude`, the `False` limitation, item keys and `'__all__'`, `exclude_defaults`, `exclude_none`, `exclude_unset` with `model_fields_set`, and the `MISSING` tip. All confirmed; nothing removed.

Method: documentation only; no commands were run.
