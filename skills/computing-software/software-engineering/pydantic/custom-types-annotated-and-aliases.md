---
id: computing-software.software-engineering.pydantic.custom-types-annotated-and-aliases
name: custom-types-annotated-and-aliases
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-custom-types, annotated, typealiastype, recursive-types, generics, type-adapter, python]
level: practitioner
status: docs-checked
description: "Build reusable Pydantic custom types with Annotated, add validation and serialization markers, use generic aliases, and define named or recursive aliases."
sources:
  - https://docs.pydantic.dev/latest/concepts/types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom types with Annotated and named aliases

Goal: define reusable constrained types and aliases the high-level way.

## Reusable constrained type

```python
from typing import Annotated
from pydantic import Field, TypeAdapter

PositiveInt = Annotated[int, Field(gt=0)]
ta = TypeAdapter(PositiveInt)
ta.validate_python(-1)  # Input should be greater than 0 [type=greater_than ...]
```

Pydantic-agnostic alternative: `Annotated[int, annotated_types.Gt(0)]`.

## Add validation, serialization and JSON Schema

```python
TruncatedFloat = Annotated[
    float,
    AfterValidator(lambda x: round(x, 1)),
    PlainSerializer(lambda x: f'{x:.1e}', return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
]
ta = TypeAdapter(TruncatedFloat)
assert ta.validate_python(1.02345) == 1.0
assert ta.dump_json(1.02345) == b'"1.0e+00"'
assert ta.json_schema(mode='validation') == {'type': 'number'}
assert ta.json_schema(mode='serialization') == {'type': 'string'}
```

## Generic aliases

```python
T = TypeVar('T')
ShortList = Annotated[list[T], Len(max_length=4)]
TypeAdapter(ShortList[int])      # at most 4 items
PositiveList = list[Annotated[T, Gt(0)]]
```

## Named aliases (v2.11+)

Implicit aliases (plain assignments) cannot be named at runtime: their JSON Schema is duplicated rather than moved into `$defs`, and recursive aliases mostly fail. Use `TypeAliasType` (or the Python 3.12 `type` statement):

```python
from typing_extensions import TypeAliasType
PositiveIntList = TypeAliasType('PositiveIntList', list[Annotated[int, Gt(0)]])
# 3.12+: type PositiveIntList = list[Annotated[int, Gt(0)]]
```

Used on two fields, the schema has one `$defs/PositiveIntList` referenced by both. Generics: `TypeAliasType('ShortList', Annotated[list[T], Len(max_length=4)], type_params=(T,))`.

**Warning:** field-specific metadata (`alias`, `default`, `deprecated`) is not allowed inside a named alias, e.g. `Annotated[int, Field(default=1)]`; only metadata applying to the type itself (constraints, JSON metadata).

## Recursive types

Always use a named alias. With `TypeAliasType` the value must be a quoted string because it is eagerly evaluated:

```python
Json = TypeAliasType(
    'Json', 'dict[str, Json] | list[Json] | str | int | float | bool | None'
)
```

With `type Json = ...` (3.12+) no quotes are needed since evaluation is lazy. `pydantic.types.JsonValue` is provided as a convenience.

## Checked

Checked 2026-11-07. Compared every claim with the types concepts page (concepts/types.md): `Annotated[int, Field(gt=0)]` and the annotated-types alternative, the `TruncatedFloat` markers and assertions, generic aliases with `Len` / `Gt`, named aliases (version-added v2.11), duplicated versus `$defs` schema, the field-specific-metadata warning, `type_params`, quoted value for `TypeAliasType` versus lazy `type` statement, and `JsonValue`. All confirmed; nothing removed.

Method: documentation only; no commands were run.
