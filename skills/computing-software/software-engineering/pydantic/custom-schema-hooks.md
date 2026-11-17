---
id: computing-software.software-engineering.pydantic.custom-schema-hooks
name: custom-schema-hooks
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-json-schema-customization, get-pydantic-core-schema, get-pydantic-json-schema, core-schema, custom-type, handler, annotated]
level: advanced
status: docs-checked
description: "Implement __get_pydantic_core_schema__ and __get_pydantic_json_schema__ to override, modify or wrap the schema Pydantic builds for a custom type or Annotated metadata."
sources:
  - https://docs.pydantic.dev/latest/concepts/json_schema/
  - https://docs.pydantic.dev/latest/internals/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema hooks for custom types and metadata

Goal: control the core schema (validation and serialization) or only the JSON schema of a custom type.

## `__get_pydantic_core_schema__(source, handler)`

Works on custom types (`x: TheType` or `Annotated[TheType, ...]`) and on `Annotated` metadata. Receives the type annotation and a `GetCoreSchemaHandler` that calls the next implementer; it behaves like a wrap field validator (input is the type, output a `core_schema`). The `source` is the annotated type for `Annotated`, and the class itself for a custom type.

Three patterns:

1. Override for a custom type: do not call `handler`; return your own schema. For the page's `CompressedString` it returns `core_schema.no_info_after_validator_function(cls._validate, core_schema.str_schema(), serialization=core_schema.plain_serializer_function_ser_schema(cls._serialize, info_arg=False, return_schema=core_schema.str_schema()))`. Calling `handler(source)` on an unknown custom type raises `PydanticSchemaGenerationError`, so you almost never call it for custom types.
2. Wrap for `Annotated` metadata: call `handler(source)`, then wrap, e.g. `core_schema.no_info_after_validator_function(self.validate, schema)`.
3. Modify: `schema = handler(source); schema['max_length'] = 10; return schema`. You must return the schema even when mutating in place.

For a fully arbitrary class, return `core_schema.no_info_plain_validator_function(validate)` without calling the handler.

Core schemas cannot be invented: pydantic-core only understands a fixed set of types (see `pydantic_core.core_schema`). Annotations apply in order: `Annotated[int, MyStrict(), MyGt()]` runs `MyStrict` first (`{'type': 'int'}` becomes strict), then `MyGt` adds `gt`.

## `__get_pydantic_json_schema__(core_schema, handler)`

Changes only the JSON schema, not validation or serialization.

```python
@classmethod
def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler):
    json_schema = handler(core_schema)
    json_schema = handler.resolve_ref_schema(json_schema)
    json_schema['examples'] = [{'name': 'John Doe', 'age': 25}]
    json_schema['title'] = 'Person'
    return json_schema
```

Prefer `WithJsonSchema` for simple overrides.

## Checked

Checked 2026-11-07. Compared every claim with the JSON Schema concepts page (concepts/json_schema.md) and the architecture page (internals/architecture.md): handler semantics, the override / wrap / modify patterns, `PydanticSchemaGenerationError`, fixed set of core schema types, annotation ordering for `MyStrict` / `MyGt`, `resolve_ref_schema`, and the `WithJsonSchema` preference. All confirmed; nothing removed.

Method: documentation only; no commands were run.
