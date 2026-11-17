---
id: computing-software.software-engineering.pydantic.discriminated-unions
name: discriminated-unions
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-discriminated-unions, discriminator, tag, tagged-union, literal, union-errors, python]
level: practitioner
status: docs-checked
description: "Define Pydantic discriminated unions with a Literal field or a callable Discriminator and Tag, nest them, and simplify verbose union validation errors."
sources:
  - https://docs.pydantic.dev/latest/concepts/unions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discriminated (tagged) unions

Goal: validate against exactly one union member chosen by a tag. It is more efficient, gives shorter errors, and the JSON Schema gets the OpenAPI `discriminator` attribute.

## String discriminator

Give each model a common field typed with `Literal` value(s), then set `discriminator` on `Field()` (or use the `Discriminator` type).

```python
class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int

class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: float

class Lizard(BaseModel):
    pet_type: Literal['reptile', 'lizard']
    scales: bool

class Model(BaseModel):
    pet: Cat | Dog | Lizard = Field(discriminator='pet_type')
    n: int
```

A missing member field reports only that member: `pet.dog.barks  Field required`. (v2.13: root models with a `Literal` root type can replace `Literal` types.)

## Callable `Discriminator` with `Tag`

When no single common field exists, pass a function. It must handle both `dict` and model instances, because callables are also used for serialization; otherwise expect warnings or runtime errors. Return `None` when no tag is found, which raises `union_tag_not_found`.

```python
def get_discriminator_value(v: Any) -> str | None:
    if isinstance(v, dict):
        return v.get('fruit', v.get('filling'))
    return getattr(v, 'fruit', getattr(v, 'filling', None))

dessert: Annotated[
    Annotated[ApplePie, Tag('apple')] | Annotated[PumpkinPie, Tag('pumpkin')],
    Discriminator(get_discriminator_value),
]
```

Works with models mixed with primitives (`Annotated[int, Tag('int')]`).

Syntax variants: `Field(discriminator='x')` or `Annotated[..., Field(discriminator='x')]` for strings; `Field(discriminator=Discriminator(...))` or `Annotated[..., Discriminator(...)]` for callables.

## Nested discriminators

Only one discriminator per field, so nest `Annotated` unions:

```python
Cat = Annotated[BlackCat | WhiteCat, Field(discriminator='color')]
Pet = Annotated[Cat | Dog, Field(discriminator='pet_type')]
```

To validate only a union, use `TypeAdapter(Pet).validate_python(...)`.

## Simplifying errors

Plain unions yield an error per member (and per recursion level). Options:

```python
Discriminator(
    model_x_discriminator,
    custom_error_type='invalid_union_member',
    custom_error_message='Invalid union member',
    custom_error_context={'discriminator': 'str_or_model'},
)
```

These set the error's `type`, `msg` and `ctx`. Also label members with `Tag`, which makes error locations read `DoubledList.0` and `StringsMap` instead of `function-after[<lambda>(), list[int]]`.

## Checked

Checked 2026-11-07. Compared every claim with the unions concepts page (concepts/unions.md): string discriminator on `Field()`, the `Cat` / `Dog` / `Lizard` example and `pet.dog.barks` error, the v2.13 root-model note, callable `Discriminator` with `Tag`, dict-and-model handling, `union_tag_not_found`, the syntax variants, nested discriminators, `TypeAdapter` tip, `custom_error_type` / `custom_error_message` / `custom_error_context` and `Tag` labels in error locations. All confirmed; nothing removed.

Method: documentation only; no commands were run.
