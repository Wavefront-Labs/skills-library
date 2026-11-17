---
id: computing-software.software-engineering.pydantic.core-schema-architecture
name: core-schema-architecture
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-core-schema-architecture, pydantic-core, core-schema, generate-schema, schema-validator, schema-serializer, plugins]
level: advanced
status: docs-checked
description: "Understand how Pydantic V2 splits work between pydantic and pydantic-core: core schemas, GenerateSchema, SchemaValidator, SchemaSerializer, and the plugin hook."
sources:
  - https://docs.pydantic.dev/latest/internals/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pydantic V2 architecture: pydantic vs pydantic-core

Goal: know where each step happens when you define, validate, serialize and generate a schema for a model.

Part of the codebase is Rust in the separate `pydantic-core` package, partly for validation and serialization performance (at the cost of limited customization of the internals).

- Model definition: `pydantic` package.
- Validation and serialization: `pydantic-core`.

## Definition

The `BaseModel` metaclass analyzes the class body and collects fields (in `model_fields`), config (`model_config`), validators and serializers, private attributes, class variables, and generic parametrization.

## Core schema

A core schema is a structured, serializable dict (typed with `TypedDict`) describing validation and serialization logic. It is the data structure exchanged between the two packages. Every core schema has a required `type` key plus type-specific keys. Definitions live in `pydantic_core.core_schema`. It is built in one place, the `GenerateSchema` class, and stored on a model as `__pydantic_core_schema__`.

You cannot define a custom core schema type: pydantic-core only understands a fixed set. This is part of why `GenerateSchema` is not exposed or documented.

Example: `foo: bool = Field(strict=True)` gives `{'type': 'bool', 'strict': True}`. A `BoolSchema` also allows `ref`, `metadata` and `serialization`. With `@field_serializer('foo', mode='plain')` the `serialization` key becomes `{'type': 'function-plain', 'function': ..., 'is_field_serializer': True, 'info_arg': False, 'return_schema': {...}}`.

## JSON Schema

`GenerateJsonSchema.generate()` is the entry point and receives the core schema; methods such as `bool_schema` return pieces (`{"type": "boolean"}`). The serialization `return_schema` feeds this.

## Customization

`__get_pydantic_core_schema__` and `__get_pydantic_json_schema__` follow a wrapper pattern. For `Annotated[int, MyStrict(), MyGt()]`, `MyStrict` runs first on `{'type': 'int'}` and sets `strict`; `MyGt` then sees the strict schema and adds `gt`. Handlers nest recursively until the plain `int` schema.

## Instance level

`Model.model_validate({'foo': 1})` calls `SchemaValidator.validate_python`, populating `__dict__`. `model.model_dump()` calls `SchemaSerializer.to_python`, reading `__dict__`.

## Plugin hook

Pydantic wraps the `SchemaValidator` in a plugin layer: installed plugins can intercept `validate_python`, `validate_json` and `validate_strings` and observe the input, result and error. Logfire uses this. Configure plugins per model through the `plugin_settings` config value.

## Checked

Checked 2026-11-07. Compared every claim with the architecture page (internals/architecture.md): pydantic versus pydantic-core split, core schema description, `GenerateSchema`, `__pydantic_core_schema__`, the `bool` and `function-plain` examples, `GenerateJsonSchema.generate`, the `MyStrict` / `MyGt` wrapper pattern, `SchemaValidator.validate_python`, `SchemaSerializer.to_python`, and the plugin hook with `plugin_settings`. All confirmed; nothing removed.

Method: documentation only; no commands were run.
