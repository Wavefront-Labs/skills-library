---
id: computing-software.software-engineering.pydantic.pydantic-alias-generators-and-priority
name: pydantic-alias-generators-and-priority
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-alias-generators, alias-generator, aliasgenerator, alias-priority, to-camel, naming-convention]
level: practitioner
status: docs-checked
description: "Generate Pydantic aliases for all fields with alias_generator, AliasGenerator and the built-in to_camel, to_pascal and to_snake, and set alias_priority."
sources:
  - https://docs.pydantic.dev/latest/concepts/alias/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: apply one naming convention to every field alias.

Set `alias_generator` in `ConfigDict`; it is a callable or an `AliasGenerator`. Built-ins: `pydantic.alias_generators.to_pascal`, `to_camel`, `to_snake`.

Callable:

```python
class Tree(BaseModel):
    model_config = ConfigDict(alias_generator=lambda field_name: field_name.upper())
    age: int
    height: float
    kind: str

t = Tree.model_validate({'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'})
t.model_dump(by_alias=True)   #> {'AGE': 12, 'HEIGHT': 1.2, 'KIND': 'oak'}
```

AliasGenerator for different validation and serialization conventions:

```python
model_config = ConfigDict(
    alias_generator=AliasGenerator(
        validation_alias=lambda field_name: field_name.upper(),
        serialization_alias=lambda field_name: field_name.title(),
    )
)
# dumps {'Age': 12, 'Height': 1.2, 'Kind': 'oak'}
```

Precedence: by default, an alias set on the `Field` beats the generated alias.

```python
def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

class Voice(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    name: str
    language_code: str = Field(alias='lang')

Voice(Name='Filiz', lang='tr-TR').model_dump(by_alias=True)
#> {'Name': 'Filiz', 'lang': 'tr-TR'}
```

`alias_priority` on the field changes this:
- `alias_priority=2`: the alias is not overridden by the generator.
- `alias_priority=1`: the alias is overridden by the generator.
- not set: if an alias is set it is not overridden; if no alias is set the generator's alias is used.
The same rules apply to `validation_alias` and `serialization_alias`.

Remember to pass `by_alias=True` (or set `serialize_by_alias=True`) when dumping, since serialization by alias is off by default.

## Checked

Checked 2026-11-07. Re-read the concepts/alias page in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
