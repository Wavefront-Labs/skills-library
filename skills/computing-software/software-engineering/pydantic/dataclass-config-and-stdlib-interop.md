---
id: computing-software.software-engineering.pydantic.dataclass-config-and-stdlib-interop
name: dataclass-config-and-stdlib-interop
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-dataclasses, dataclass-config, stdlib-dataclass, revalidate-instances, arbitrary-types-allowed, python]
level: practitioner
status: docs-checked
description: "Configure Pydantic dataclasses, inherit from or wrap stdlib dataclasses, use them inside BaseModel, handle arbitrary types, and detect Pydantic dataclasses."
sources:
  - https://docs.pydantic.dev/latest/concepts/dataclasses/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dataclass config and stdlib dataclass interop

Goal: set configuration on dataclasses and mix stdlib and Pydantic dataclasses safely.

## Config (two options)

```python
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

@dataclass(config=ConfigDict(validate_assignment=True))
class MyDataclass1:
    a: int

@dataclass
class MyDataclass2:
    a: int
    __pydantic_config__ = ConfigDict(validate_assignment=True)
```

## Inherit from stdlib dataclasses

Inherited fields from (nested or not) stdlib dataclasses are validated automatically:

```python
@dataclasses.dataclass
class Z:
    z: int

@dataclasses.dataclass
class Y(Z):
    y: int = 0

@pydantic.dataclasses.dataclass
class X(Y):
    x: int = 0

X(x=b'1', y='2', z='3')   # X(z=3, y=2, x=1)
```

The decorator applied to a stdlib dataclass creates a new subclass: `PydanticA = pydantic.dataclasses.dataclass(A)`; `PydanticA(a='1')` gives `A(a=1)`.

## Stdlib dataclass inside BaseModel

When a stdlib dataclass is a field of a model, Pydantic dataclass, or `TypeAdapter`, validation is applied with the same configuration, so stdlib and Pydantic dataclasses are functionally equivalent as annotations. Constructing the stdlib dataclass itself validates nothing (`User(name=['not','a','string'])` succeeds). To have the model revalidate instances, set `model_config = ConfigDict(revalidate_instances='always')`; then `Foo(user=user)` raises `user.name  Input should be a valid string`. Frozen stdlib dataclasses still raise `dataclasses.FrozenInstanceError` on assignment.

## Custom types: `arbitrary_types_allowed`

If a stdlib dataclass has a field of an unknown class, using it in a model raises `PydanticSchemaGenerationError`. Set `ConfigDict(arbitrary_types_allowed=True)` on the model; the config pushes down to the nested vanilla dataclass.

```python
class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dc: DC
    other: str
```

The alternative named by the error is implementing `__get_pydantic_core_schema__` on the type. If you call `handler(<some type>)` in it and see the error, use `handler.generate_schema(<some type>)`.

## Detect Pydantic dataclasses

`dataclasses.is_dataclass()` is `True` for both kinds. Use `pydantic.dataclasses.is_pydantic_dataclass(cls)` to tell them apart: `False` for the plain stdlib class, `True` for the wrapped one.

## Checked

Checked 2026-11-07. Compared every claim with the dataclasses concepts page (concepts/dataclasses.md): `config=` argument and `__pydantic_config__`, inheriting from stdlib dataclasses with the `X(x=b'1', y='2', z='3')` result, applying the decorator to a stdlib dataclass, validation of stdlib dataclasses inside models with `revalidate_instances='always'`, `FrozenInstanceError`, `arbitrary_types_allowed` pushing down to the nested dataclass, the `PydanticSchemaGenerationError` hint about `handler.generate_schema`, and `is_pydantic_dataclass`. All confirmed; nothing removed.

Method: documentation only; no commands were run.
