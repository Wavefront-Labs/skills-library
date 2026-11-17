---
id: computing-software.software-engineering.pydantic.customize-json-schema
name: customize-json-schema
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-json-schema-customization, json-schema-extra, with-json-schema, skip-json-schema, title-generator, field, examples]
level: practitioner
status: docs-checked
description: "Customize Pydantic JSON Schema output with Field title/description/examples, json_schema_extra, title generators, WithJsonSchema and SkipJsonSchema."
sources:
  - https://docs.pydantic.dev/latest/concepts/json_schema/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customize JSON Schema per field or model

Goal: adjust titles, descriptions, examples or whole fragments of the generated schema.

## Field level

Parameters used only for the schema: `title`, `description`, `examples`, `json_schema_extra`, `field_title_generator`.

```python
class User(BaseModel):
    age: int = Field(description='Age of the user')
    email: Annotated[EmailStr, Field(examples=['marcelo@mail.com'])]
    name: str = Field(title='Username')
    password: SecretStr = Field(json_schema_extra={'title': 'Password', 'examples': ['123456']})
```

`SecretStr` renders with `format: password` and `writeOnly: true`.

## Model level (ConfigDict)

Relevant options: `title`, `json_schema_extra`, `json_schema_mode_override`, `field_title_generator`, `model_title_generator`.

- `field_title_generator(field_name, field_info)` returns a title; set it on `Field` for one field or on `ConfigDict` for all fields.
- `model_title_generator(model)` receives the class: a function returning `f'Title-{model.__name__}'` yields title `Title-Person` for a `Person` model.

## `json_schema_extra`

Accepts a dict or a callable, at field or model level.

- Dict: `ConfigDict(json_schema_extra={'examples': [{'a': 'Foo'}]})`.
- Callable mutates the schema: `def pop_default(s): s.pop('default')` with `Field(default=1, json_schema_extra=pop_default)` removes `default`.
- From v2.9, dicts from annotated types merge additively (previously overridden): stacking `{'key1': 'value1'}` and `{'key2': 'value2'}` yields both keys. Mixing dict and callable specifications is not supported.

## `WithJsonSchema`

Overrides the entire schema for a type, so include `type` yourself. Preferred over implementing `__get_pydantic_json_schema__` for custom types. Useful for types with no default schema such as `Callable`.

```python
MyInt = Annotated[int, WithJsonSchema({'type': 'integer', 'examples': [1, 0, -1]})]
```

For fields with validators, the page recommends the `json_schema_input_type` argument of the validator instead of `WithJsonSchema`.

## `SkipJsonSchema`

`pydantic.json_schema.SkipJsonSchema` omits a field, or part of a field's specification, from the generated schema (see the API docs for details).

## Checked

Checked 2026-11-07. Compared every claim with the JSON Schema concepts page (concepts/json_schema.md): field-only schema parameters, model-level ConfigDict options, title generators, `json_schema_extra` as dict or callable, additive merging from v2.9, no mixing of dict and callable, `WithJsonSchema`, `json_schema_input_type` recommendation, `SkipJsonSchema`, and `format: password` / `writeOnly` for `SecretStr`. Reworded the `model_title_generator` example, which the page writes as a named function, not a lambda.

Method: documentation only; no commands were run.
