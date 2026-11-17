---
id: computing-software.software-engineering.pydantic.generate-json-schema
name: generate-json-schema
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-json-schema-generation, model-json-schema, typeadapter, json-schema, openapi, ref-template, defs]
level: practitioner
status: docs-checked
description: "Generate JSON Schema from Pydantic models and TypeAdapters, pick validation or serialization mode, build a top-level schema, and rewrite $ref locations."
sources:
  - https://docs.pydantic.dev/latest/concepts/json_schema/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generate JSON Schema

Goal: produce a JSON Schema (Draft 2020-12 compliant, also OpenAPI 3.1.0) from a model or any type.

## Entry points

- `BaseModel.model_json_schema()` returns a jsonable dict for a model.
- `TypeAdapter(tp).json_schema()` does the same for any type, e.g. `TypeAdapter(list[int]).json_schema()` gives `{'items': {'type': 'integer'}, 'type': 'array'}`, and `TypeAdapter(Cat | Dog)` yields `anyOf` of `$ref`s into `$defs`.
- "Jsonable" means `json.dumps(schema)` is valid JSON. These are not `model_dump_json` / `dump_json`, which serialize instances to strings.

## Mode

`mode='validation'` (default) or `mode='serialization'`. They can differ: for `a: Decimal = Decimal('12.34')`, validation gives `anyOf: [{'type': 'number'}, {'type': 'string'}]` while serialization gives `{'type': 'string'}` (the page also notes `Decimal` is exposed and serialized as a string).

## Top-level schema for several models

```python
from pydantic.json_schema import models_json_schema

_, top_level_schema = models_json_schema(
    [(Model, 'validation'), (Bar, 'validation')], title='My Schema'
)
```

The result has only `$defs` (models and their sub-models) plus the `title`.

## Change `$ref` locations

Pass `ref_template` (definitions always live under `$defs`, only the reference prefix changes). The page names `model_json_schema()` and `model_dump_json()` as accepting it, and its example uses the TypeAdapter method:

```python
adapter.json_schema(ref_template='#/components/schemas/{model}')
# property a -> {"$ref": "#/components/schemas/Foo"}
```

## Behaviors to know

- `Optional` fields allow `null`.
- Sub-models go in `$defs` and are referenced; sub-models modified through `Field` (custom title, description, default) are included inline recursively.
- A model's `description` comes from its docstring or the `Field` `description` argument.
- Aliases are used as keys by default; `by_alias=False` uses property names.
- `namedtuple` is not preserved as a namedtuple.
- Type-to-format mapping priority: JSON Schema Core, JSON Schema Validation, OpenAPI data types, then the standard `format` field for Pydantic extensions of `string` subtypes.
- Keys are sorted alphabetically by default, but `properties` keeps field definition order.

## Checked

Checked 2026-11-07. Compared every claim with the JSON Schema concepts page (concepts/json_schema.md): Draft 2020-12 and OpenAPI 3.1.0, `model_json_schema` / `TypeAdapter.json_schema`, `mode` values and the `Decimal` example, `models_json_schema`, `ref_template`, the miscellaneous notes (Optional, sub-models, description, aliases, namedtuple, sorting) and the format priority list. All confirmed; nothing removed.

Method: documentation only; no commands were run.
