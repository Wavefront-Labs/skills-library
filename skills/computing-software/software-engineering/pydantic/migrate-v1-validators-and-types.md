---
id: computing-software.software-engineering.pydantic.migrate-v1-validators-and-types
name: migrate-v1-validators-and-types
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-v1-migration, field-validator, model-validator, typeadapter, optional-required, union-mode, constrained-types]
level: practitioner
status: docs-checked
description: "Migrate V1 validators and type behaviour to Pydantic V2: field_validator, model_validator, validate_call, TypeAdapter, Optional rules, unions, regex, URLs, Constrained types."
sources:
  - https://docs.pydantic.dev/latest/migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: replace V1 validator APIs and adjust to V2 coercion behaviour.

## Validators
- `@validator` -> `@field_validator`; `@root_validator` -> `@model_validator` (signatures changed). `each_item` is gone: annotate the type argument, e.g. `list[Annotated[int, Field(ge=0)]]`.
- `field`/`config` validator arguments are gone; use `info: ValidationInfo`: `info.config`, `cls.model_fields[info.field_name]`.
- `always=True` -> `Field(validate_default=True)`.
- A `@model_validator` may receive a model instance, not a dict, e.g. on assignment with `validate_assignment=True`.
- Deprecated `@root_validator` needs `skip_on_failure=True`.
- `TypeError` raised in a validator is no longer converted into `ValidationError` (applies to all validation decorators).
- `allow_reuse` is unnecessary: delete it. Redefinition is only an error inside a single class.
- `@validate_arguments` -> `@validate_call`; attributes like `raw_function` and `validate` are not preserved.

## Types and coercion
- Input types are not preserved: `Mapping[str, int]` with a `dict` subclass returns a plain `dict`. To restore, use `Annotated[T, WrapValidator(...)]` returning `type(value)(handler(value))`. Subclasses of `BaseModel` and dataclasses are preserved.
- `float` to `int` only if the decimal part is zero: `Model(x=10.0)` gives 10, `10.2` fails with `int_from_float`.
- `int`, `float`, `Decimal` to `str` coercion is off by default (`coerce_numbers_to_str`). Iterables of pairs no longer validate as `dict`.
- Unions keep the input type when possible: `x: int | str` given `'1'` stays `'1'`. For V1 behaviour use `Field(union_mode='left_to_right')`.
- `Optional[str]` without default is required but nullable. Table: `f1: str` required; `f2: str = 'abc'` optional; `f3: Optional[str]` required, may be `None`; `f4: Optional[str] = None` optional; `f6: Any` required; `f7: Any = None` optional.
- Regex uses the Rust regex crate (linear time; no look-arounds or backreferences). Use the `regex_engine` config to get Python's `re`.
- URL and Dsn types no longer inherit `str`; use `str(url)`. `AnyUrl('https://google.com')` stringifies as `https://google.com/`.
- `Constrained*` classes removed: `MyInt = Annotated[int, Field(ge=0)]`; `ConstrainedStr` -> `StringConstraints`.
- `parse_obj_as`/`schema_of` -> `TypeAdapter(list[int]).validate_python(...)`, `.json_schema()`.
- Custom types: `__get_validators__` -> `__get_pydantic_core_schema__`; `__modify_schema__` -> `__get_pydantic_json_schema__`.
- `BaseSettings` moved to `pydantic-settings`; Color and payment card types moved to `pydantic-extra-types`.
- mypy: `plugins = pydantic.mypy` (add `pydantic.v1.mypy` for V1 features).

## Checked

Checked 2026-11-07. Compared every claim with the migration guide (migration.md): validator replacements and the `each_item` change, `info.config` / `info.field_name`, `always=True` and `validate_default`, `skip_on_failure`, `TypeError` handling, `allow_reuse`, `validate_call`, input type preservation, float to int, `coerce_numbers_to_str`, union short-circuiting and `union_mode`, the Optional table, the Rust regex engine and `regex_engine`, URL types, `Constrained*`, `TypeAdapter`, custom type hooks, moved packages and the mypy plugin line. All confirmed; nothing removed.

Method: documentation only; no commands were run.
