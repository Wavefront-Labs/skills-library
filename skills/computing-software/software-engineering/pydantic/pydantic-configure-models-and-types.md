---
id: computing-software.software-engineering.pydantic.pydantic-configure-models-and-types
name: pydantic-configure-models-and-types
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-model-config, configdict, model-config, with-config, config-inheritance, plugin-settings]
level: practitioner
status: docs-checked
description: "Set Pydantic ConfigDict on models, dataclasses, TypeAdapter, TypedDict and stdlib dataclasses, and understand inheritance and propagation."
sources:
  - https://docs.pydantic.dev/latest/concepts/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: put configuration in the right place and know where it applies.

BaseModel, two ways:

```python
class Model(BaseModel):
    model_config = ConfigDict(str_max_length=5)   # a plain dict also works
    v: str

class Model2(BaseModel, frozen=True):   # class arguments are understood by type checkers
    a: str
```
`Model(v='abcdef')` fails with "String should have at most 5 characters" (string_too_long).

Pydantic dataclass: `@dataclass(config=ConfigDict(str_max_length=10, validate_assignment=True))` (from `pydantic.dataclasses`).

TypeAdapter: `TypeAdapter(list[str], config=ConfigDict(coerce_numbers_to_str=True))`. Config cannot be passed if the wrapped type already supports config (usage error).

Stdlib dataclasses and TypedDict: set the `__pydantic_config__` class attribute, or use `@with_config(ConfigDict(str_to_lower=True))` (avoids type-checking errors with TypedDict).

`@validate_call` also accepts config (see the validation decorator docs).

Inheritance: configuration is inherited, so a shared parent class changes behaviour globally. Subclass config is merged with the parent's:

```python
class Parent(BaseModel):
    model_config = ConfigDict(extra='allow', str_to_lower=False)
class Model(Parent):
    model_config = ConfigDict(str_to_lower=True)
    x: str
Model.model_config   #> {'extra': 'allow', 'str_to_lower': True}
```
Warning: with multiple bases Pydantic does not follow the MRO (known issue 9992).

Propagation:
- Models and Pydantic dataclasses: not propagated; each is its own configuration boundary. A parent with `str_to_lower=True` does not lowercase a nested `User` model's name.
- Stdlib dataclasses and TypedDicts used as field types: parent config is propagated unless the type has its own config (for example `@with_config(str_to_lower=False)`).

Plugin settings: `plugin_settings` passes a dict keyed by plugin name to Pydantic plugins. Example from the docs: `class User(BaseModel, plugin_settings={'logfire': {'record': 'failure'}})`.

## Checked

Checked 2026-11-07. Re-read the concepts/config page in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
