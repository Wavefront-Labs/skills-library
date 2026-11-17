---
id: computing-software.software-engineering.pydantic.custom-types-core-schema
name: custom-types-core-schema
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-custom-types, get-pydantic-core-schema, getpydanticschema, third-party-types, generic-classes, python]
level: advanced
status: docs-checked
description: "Hook into pydantic-core with __get_pydantic_core_schema__ or GetPydanticSchema to support custom classes, third-party types and generic containers."
sources:
  - https://docs.pydantic.dev/latest/concepts/types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom types via `__get_pydantic_core_schema__`

Goal: customise how Pydantic builds the `pydantic-core` schema for a class or annotation. This API is the area most likely to change; prefer built-ins (`annotated-types`, `Field`, `BeforeValidator`) first.

It is middleware-like, similar to wrap validators: you receive `source_type` (not necessarily the class, e.g. for generics) and a `handler`. You may call the handler as-is, change the type first, change the returned schema, or not call it.

## On a type

```python
class Username(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))
```

## As an Annotated marker

```python
@dataclass(frozen=True)  # frozen makes it hashable; needed for unions like Username | None
class MyAfterValidator:
    func: Callable[[Any], Any]

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_after_validator_function(self.func, handler(source_type))

Username = Annotated[str, MyAfterValidator(str.lower)]
```

## Third-party types

Put `__get_pydantic_core_schema__` (and optionally `__get_pydantic_json_schema__`) on a marker class and annotate: `Annotated[ThirdPartyType, _Marker]`. The page builds `core_schema.json_or_python_schema(json_schema=..., python_schema=core_schema.union_schema([core_schema.is_instance_schema(T), from_int_schema]), serialization=core_schema.plain_serializer_function_ser_schema(lambda i: i.x))`, where `from_int_schema = core_schema.chain_schema([core_schema.int_schema(), core_schema.no_info_plain_validator_function(fn)])`. JSON Schema reuses `handler(core_schema.int_schema())`.

## Less boilerplate

```python
Annotated[str, GetPydanticSchema(
    lambda tp, handler: core_schema.no_info_after_validator_function(lambda x: x * 2, handler(tp))
)]
```

## Generic classes

Use `typing.get_origin` / `get_args` on `source_type`, then `handler.generate_schema(item_tp)`. Do **not** call `handler(get_args(source_type)[0])`: you want an unrelated schema for the parameter, not one influenced by surrounding `Annotated` metadata. A generic class with this classmethod does not need `arbitrary_types_allowed`. The page's `Owner[ItemType]` and `MySequence(Sequence[T])` examples combine `is_instance_schema(cls)` with the item/`Sequence[args[0]]` schema.

## Summary order

1. Use `Annotated` hooks like `AfterValidator` and `Field`.
2. Else `GetPydanticSchema` or a marker class.
3. Else implement the method on the type itself.

## Checked

Checked 2026-11-07. Compared every claim with the types concepts page (concepts/types.md): middleware-like API with `source_type` and `handler`, the `Username` and `MyAfterValidator` examples including the `frozen=True` hashing note, the third-party-type schema built from `json_or_python_schema`, `GetPydanticSchema`, `handler.generate_schema` versus `handler(...)` for generic parameters, the `arbitrary_types_allowed` note and the summary order. All confirmed; nothing removed.

Method: documentation only; no commands were run.
