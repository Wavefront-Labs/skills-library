---
id: computing-software.web-development.fastapi.body-field-validation
name: body-field-validation
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, request-body, pydantic, field, json-schema-extra, validation]
level: practitioner
status: docs-checked
description: "Add validation and metadata inside Pydantic models with Field imported from pydantic (not fastapi), and pass json_schema_extra into the OpenAPI schema."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/body-fields.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Field() in body models

Goal: validate model attributes the way `Query` validates parameters.

## Rules
- Import `Field` directly from `pydantic`, not from `fastapi` as `Query`, `Path` and `Body` are.
- Use it on model attributes. It takes the same parameters as `Query`, `Path` and `Body`; each attribute then has the same structure as a path operation parameter (type, default, `Field`).
- `json_schema_extra` on `Field`, `Query`, `Body` and similar adds extra information to the generated JSON Schema.

## Caution
Extra keys in `json_schema_extra` also appear in the application's OpenAPI schema. They may not be part of the OpenAPI specification, so some tools (for example the OpenAPI validator at validator.swagger.io) may not work with the schema.

## Background
`Query`, `Path` and others create subclasses of `Param`, itself a subclass of Pydantic's `FieldInfo`; `Field` returns a `FieldInfo` too.

## Checked

Method: docs-only read of cited pages, 2026-11-08
