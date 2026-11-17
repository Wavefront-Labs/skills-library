---
id: computing-software.software-engineering.pydantic.fix-model-definition-errors
name: fix-model-definition-errors
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-usage-errors, model-config, create-model, rootmodel, typeadapter, dataclass, pydantic-user-error]
level: practitioner
status: docs-checked
description: "Fix Pydantic PydanticUserError codes raised when defining models: missing annotations, overridden fields, create_model, RootModel, TypeAdapter config, dataclasses."
sources:
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Usage errors when defining models and configs

Goal: map a model-definition `PydanticUserError.code` to its fix.

## Fields

- `model-field-missing-annotation`: `a = Field('foobar')` or `b = None` without annotations. Annotate, mark non-fields as `ClassVar[str]`, or set `ConfigDict(ignored_types=(IgnoredType,))`.
- `model-field-overridden`: a parent field overridden by a non-annotated attribute (`a = 123.0` in a subclass of `a: float`). Annotate it.
- `model-config-invalid-field-name`: a field named `model_config`.
- `unevaluable-type-annotation`: name clash such as `date: date`; use `datetime.date`.
- `schema-for-unknown-type`: no CoreSchema for a type (e.g. `x: 43 = 123`).
- `circular-reference-schema`: valid alias `type A = list[A] | None`; invalid `type A = A` or `B = C`, `C = B`.
- `base-model-instantiated`: `BaseModel()` called directly.

## `create_model`

- `create-model-field-definitions`: bad definition such as `foo=(str, 'default value', 'more')`.
- `create-model-namespace`: a `__namespace__` key clashes with a field, or is `__annotations__`, `__module__`, `__qualname__`, `__doc__` or `model_config`. Use `__config__` for config.

## Config

- `type-adapter-config-unused`: `TypeAdapter(MyTypedDict, config=...)` for `BaseModel`, `TypedDict` or dataclass. Instead set `__pydantic_config__ = ConfigDict(strict=True)` on the TypedDict (or `model_config` on a model).
- `root-model-extra`: `RootModel` subclass with `model_config = {'extra': 'allow'}`.
- `validate-by-alias-and-name-false`: both `validate_by_alias` and `validate_by_name` set to `False` is disallowed because attributes could not be populated.
- `with-config-on-model`: `with_config` on a `BaseModel` subclass; use `model_config`.

## Dataclasses

- `dataclass-on-model`: Pydantic `@dataclass` applied to a `BaseModel` subclass.
- `dataclass-init-false-extra-allow`: `extra='allow'` with a field that has `init=False`. Message: "Field a has `init=False` and dataclass has config setting `extra="allow"`. This combination is not allowed."
- `clashing-init-and-init-var`: `Field(init=False, init_var=True)` are mutually exclusive.

## JSON schema

`invalid-for-json-schema`: a type with no JSON schema (e.g. `Callable[..., object]`) during `model_json_schema()`; see the custom JSON schema generator skill to omit it.

Gotcha: the page also lists `json-schema-already-used`, raised when a generator instance is reused.

## Checked

Checked 2026-11-07. Compared every claim with the usage errors page (errors/usage_errors.md): all listed codes, their triggers and fixes, the `create_model` namespace keys, the `TypeAdapter` config fix, the `root-model-extra` case, the dataclass `init` messages, and the JSON schema codes. All confirmed; nothing removed.

Method: documentation only; no commands were run.
