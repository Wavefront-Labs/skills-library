---
id: computing-software.software-engineering.pydantic.pydantic-dataclasses
name: pydantic-dataclasses
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-dataclasses, dataclass, typeadapter, generic-dataclass, field, python]
level: practitioner
status: docs-checked
description: "Get Pydantic validation on dataclasses with pydantic.dataclasses.dataclass, know how they differ from BaseModel, and handle generics and Field usage."
sources:
  - https://docs.pydantic.dev/latest/concepts/dataclasses/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pydantic dataclasses

Goal: validate stdlib-style dataclasses without `BaseModel`.

```python
from datetime import datetime
from pydantic.dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None = None

User(id='42', signup_ts='2032-06-21T12:00')
# User(id=42, name='John Doe', signup_ts=datetime.datetime(2032, 6, 21, 12, 0))
```

Pydantic dataclasses are **not** a replacement for models; they give stdlib dataclass behaviour plus validation. Sometimes a model is the better choice.

## Same as models

- Configuration support (but no `model_config` attribute; see the config skill).
- Nested classes.
- Arguments used to instantiate are copied.

## Differences

- No `model_validate`, `model_dump`, JSON Schema methods. Wrap with `TypeAdapter`:

```python
TypeAdapter(Foo).dump_python(foo)             # {'f': 1}
TypeAdapter(Foo).validate_python({'f': 1})    # Foo(f=1)
```

- `extra` behaviour: extra data is not included in serialization, and values cannot be customised via `__pydantic_extra__`.
- Generic dataclasses work, but a parameterised one does not validate: `Foo[int](f='not_an_int')` returns `Foo(f='not_an_int')` because `Foo[int]` is a generic alias, treated like `Foo[Any]`. Wrap `Foo[int]` in a `TypeAdapter` instead.

## Field definitions

Both Pydantic `Field()` and `dataclasses.field()` work, and the decorator accepts the standard decorator arguments plus `config`:

```python
@dataclass
class User:
    id: int
    name: str = 'John Doe'
    friends: list[int] = dataclasses.field(default_factory=lambda: [0])
    age: int | None = dataclasses.field(
        default=None,
        metadata={'title': 'The age of the user', 'description': 'do not lie!'},
    )
    height: int | None = Field(default=None, title='The height in cm', ge=50, le=300)

User(id='42', height='250')
# User(id=42, name='John Doe', friends=[0], age=None, height=250)
```

## Validators and hooks

`field_validator` works as usual. `__post_init__()` is supported and runs **between** the before and after model validators. A before model validator receives `ArgsKwargs` (from `pydantic_core`), unlike models.

## Rebuilding

`rebuild_dataclass()` (in `pydantic.dataclasses`) rebuilds the core schema, like rebuilding a model schema.

## Checked

Checked 2026-11-07. Re-read concepts/dataclasses in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
