---
id: computing-software.software-engineering.pydantic.custom-json-schema-generator
name: custom-json-schema-generator
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-json-schema-generation, generate-json-schema, schema-generator, pydantic-omit, sorting, json-schema-dialect]
level: advanced
status: docs-checked
description: "Subclass GenerateJsonSchema to change Pydantic's global JSON Schema generation: add keys, omit unsupported fields, disable key sorting."
sources:
  - https://docs.pydantic.dev/latest/concepts/json_schema/
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customize the JSON Schema generation process

Goal: change schema output globally rather than per field.

`GenerateJsonSchema` translates a pydantic-core schema into JSON Schema, split into small overridable methods. Methods that produce JSON schema accept `schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema`; pass your subclass.

## Add keys to the top level

```python
class MyGenerateJsonSchema(GenerateJsonSchema):
    def generate(self, schema, mode='validation'):
        json_schema = super().generate(schema, mode=mode)
        json_schema['title'] = 'Customize title'
        json_schema['$schema'] = self.schema_dialect
        return json_schema

MyModel.model_json_schema(schema_generator=MyGenerateJsonSchema)
# adds 'title': 'Customize title' and '$schema': 'https://json-schema.org/draft/2020-12/schema'
```

## Omit fields that have no JSON schema

By default a field such as `Callable[..., object]` makes `model_json_schema()` raise `PydanticUserError` with code `invalid-for-json-schema`. Override `handle_invalid_for_json_schema` to raise `PydanticOmit` and those fields are dropped:

```python
from pydantic_core import PydanticOmit

class MyGenerateJsonSchema(GenerateJsonSchema):
    def handle_invalid_for_json_schema(self, schema, error_info: str) -> JsonSchemaValue:
        raise PydanticOmit
```

With `Example` having `name: str = 'example'` and `function: Callable = example_callable`, `model_json_schema(schema_generator=MyGenerateJsonSchema, mode='validation')` keeps only `name`.

## Disable sorting

Pydantic recursively sorts schema keys alphabetically, skipping the values of `properties` (field order is preserved). Override `sort(self, value, parent_key=None)` to return `value` unchanged and the original order of fields and `json_schema_extra` keys is kept.

## Gotcha

The usage-errors page ("JSON schema already used") says an error is raised when the JSON schema generator has already been used to generate a schema; create a new instance to generate a new one.

## Checked

Checked 2026-11-07. Compared every claim with the JSON Schema concepts page (concepts/json_schema.md) and the usage errors page (errors/usage_errors.md): `schema_generator` argument, `generate` override with `schema_dialect`, `handle_invalid_for_json_schema` raising `PydanticOmit`, `sort` override, the `invalid-for-json-schema` code for `Callable[..., object]`, and the `json-schema-already-used` text. All confirmed; nothing removed.

Method: documentation only; no commands were run.
