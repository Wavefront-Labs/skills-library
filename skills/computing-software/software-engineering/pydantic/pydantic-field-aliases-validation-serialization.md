---
id: computing-software.software-engineering.pydantic.pydantic-field-aliases-validation-serialization
name: pydantic-field-aliases-validation-serialization
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-aliases, alias, validation-alias, serialization-alias, aliaspath, aliaschoices, by-alias]
level: practitioner
status: docs-checked
description: "Define Pydantic aliases with alias, validation_alias, serialization_alias, AliasPath and AliasChoices, and control alias use per call or per model."
sources:
  - https://docs.pydantic.dev/latest/concepts/alias/
  - https://docs.pydantic.dev/latest/concepts/fields/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: accept and emit differently named keys.

Field parameters:
- `alias` (str): used for validation and serialization.
- `validation_alias` (str, `AliasPath` or `AliasChoices`): validation only.
- `serialization_alias` (str): serialization only.
`validation_alias` beats `alias` for validation; `serialization_alias` beats `alias` for serialization.

```python
class User(BaseModel):
    name: str = Field(alias='username')

user = User(username='johndoe')
user.model_dump(by_alias=True)   #> {'username': 'johndoe'}
```
`model_dump()` has `by_alias=False` by default, so aliases are not emitted unless you pass `by_alias=True` or set `ConfigDict(serialize_by_alias=True)`. The docs note this is inconsistent with validation (aliases on by default) and expected to change in V3.

AliasPath digs into nested data; AliasChoices lists alternatives, earlier ones win:

```python
first_name: str = Field(validation_alias=AliasPath('names', 0))
address: str = Field(validation_alias=AliasPath('contact', 'address'))
first_name: str = Field(validation_alias=AliasChoices('first_name', AliasPath('names', 0)))
```
If both `first_name` and `fname` are given, `first_name` wins and `fname` is treated as extra data.

Model-level validation config:
- `validate_by_alias`: default `True`.
- `validate_by_name`: default `False`. With both `True`, either works; if both keys are supplied the alias takes precedence.
- Setting both to `False` raises a usage error.

Per-call flags on `model_validate()`, `model_validate_json()`, `model_validate_strings()` and TypeAdapter validation methods: `by_alias` (default `True`) and `by_name` (default `False`); both `False` is an error. These cross nested-model config boundaries; ConfigDict settings do not.

Type checkers: they use `alias` (not `validation_alias`) to synthesize `__init__`, and with `validate_by_name=True` they reject the field name. Workaround: `Annotated[str, Field(alias='username')]` with `validate_by_name=True, validate_by_alias=True`, or set `alias` plus `serialization_alias` equal to the field name.

## Checked

Checked 2026-11-07. Re-read concepts/alias and concepts/fields in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
