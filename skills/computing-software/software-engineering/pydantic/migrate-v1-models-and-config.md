---
id: computing-software.software-engineering.pydantic.migrate-v1-models-and-config
name: migrate-v1-models-and-config
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-v1-migration, bump-pydantic, model-dump, model-config, pydantic-v1-namespace, basemodel-renames, field-changes]
level: practitioner
status: docs-checked
description: "Migrate Pydantic V1 code to V2: bump-pydantic, pydantic.v1 fallback, BaseModel method renames, Field and config setting changes, dataclass and generic-model changes."
sources:
  - https://docs.pydantic.dev/latest/migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: move a V1 codebase to V2 using the guide's renames and removals. The guide covers V1 to V2 only.

## Tooling
`pip install bump-pydantic` (beta), then `cd /path/to/repo_folder && bump-pydantic my_package`. To keep V1 temporarily: `pip install "pydantic==1.*"`, or import `from pydantic.v1 import BaseModel` (the `pydantic.v1` namespace was removed in V3). With `pydantic>=1.10.17` the `.v1` namespace exists in V1 too, so replace `pydantic<2` with `pydantic>=1.10.17` and rewrite `from pydantic.<module> import X` to `from pydantic.v1.<module> import X`.

## BaseModel renames (V1 -> V2)
`__fields__` -> `model_fields`; `construct()` -> `model_construct()`; `copy()` -> `model_copy()`; `dict()` -> `model_dump()`; `json()` -> `model_dump_json()`; `json_schema()` -> `model_json_schema()`; `parse_obj()` -> `model_validate()`; `update_forward_refs()` -> `model_rebuild()`. Old names remain deprecated and emit `DeprecationWarning`.
- `parse_raw`/`parse_file` deprecated: use `model_validate_json`, or load data then `model_validate`.
- `from_orm` deprecated: `model_validate` with `from_attributes=True`.
- `__root__` replaced by `RootModel` (no `arbitrary_types_allowed`).
- `json_encoders` in config is deprecated; use `@field_serializer`, `@model_serializer`, `@computed_field`.
- `__eq__`: only equal to other `BaseModel` instances with the same type, field values, extras and private attributes; never equal to dicts.
- Generic models: use `class MyGenericModel(BaseModel, Generic[T])` (no `GenericModel`). Avoid `isinstance(m, MyGenericModel[int])`; subclass `class MyIntModel(MyGenericModel[int])` instead.
- Subclass instances nested in a field are serialized using only the fields of the annotated type.

## Field
Removed: `const`, `unique_items`, `final` (use `typing.Final`). Renamed: `min_items`/`max_items` -> `min_length`/`max_length`, `allow_mutation` -> `frozen`, `regex` -> `pattern`. Extra JSON-schema data goes in `json_schema_extra`. `alias` returns `None` when unset. Constraints are no longer pushed into generics: use `list[Annotated[str, Field(pattern=".*")]]`.

## Config
Use `model_config = {...}` (the `Config` class is deprecated); multiple-inheritance settings merge, later bases win. Renames: `allow_population_by_field_name` -> `populate_by_name`, `anystr_lower/strip_whitespace/upper` -> `str_to_lower/str_strip_whitespace/str_to_upper`, `keep_untouched` -> `ignored_types`, `max_anystr_length`/`min_anystr_length` -> `str_max_length`/`str_min_length`, `orm_mode` -> `from_attributes`, `schema_extra` -> `json_schema_extra`, `validate_all` -> `validate_default`. Removed: `error_msg_templates`, `fields`, `getter_dict`, `smart_union`, `json_loads`, `json_dumps`, `copy_on_model_validation`, `post_init_call`.

## Dataclasses
`__post_init__` now runs after validation (`__post_init_post_parse__` removed); no `extra='allow'`; no `__pydantic_model__` (wrap with `TypeAdapter`); when used as fields, dataclasses no longer accept tuples as validation input (use dicts).

## Checked

Checked 2026-11-07. Compared every claim with the migration guide (migration.md): `bump-pydantic` (beta) usage, `pydantic==1.*`, the `pydantic.v1` namespace and its V3 removal, the `>=1.10.17` steps, the `BaseModel` rename table, `parse_raw` / `parse_file` / `from_orm`, `RootModel`, `json_encoders`, `__eq__` rules, generic model changes, subclass serialization, the `Field` removals and renames, and the config renames and removals. Reworded the dataclass tuple note to say it applies to dataclasses used as fields. Not every removed config key on the page is listed in the skill (`allow_mutation` is under `Field`; `underscore_attrs_are_private` is omitted).

Method: documentation only; no commands were run.
