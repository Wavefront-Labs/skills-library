---
id: computing-software.web-development.fastapi.schema-extra-examples
name: schema-extra-examples
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, examples, openapi-examples, json-schema-extra, model-config, swagger-ui, openapi]
level: practitioner
status: docs-checked
description: "Declare request example data in FastAPI with json_schema_extra, Field examples, Body examples and the OpenAPI-specific openapi_examples parameter."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/schema-extra-example.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request examples

## Options
- Pydantic model: set `model_config` with a `"json_schema_extra"` dict containing `examples`; it is added as-is to the model JSON Schema and used in the docs. Any extra data (e.g. frontend metadata) can go there.
- `Field(examples=[...])` on a model field.
- `examples=[...]` (a list) on `Path()`, `Query()`, `Header()`, `Cookie()`, `Body()`, `Form()`, `File()`. It lands in the JSON Schema inside OpenAPI.
- Several `examples` are kept in the JSON Schema, but Swagger UI (as of 2023-08-26, per the docs) did not show multiple JSON Schema examples.
- Workaround: `openapi_examples` on the same functions (FastAPI 0.103.0 and above). It is a dict whose keys name examples; each value may have `summary`, `description` (Markdown), `value`, or `externalValue` (a URL, less widely supported). It sits on the path operation in OpenAPI, not in the JSON Schema, and Swagger UI shows it.

## Versions
- OpenAPI 3.1.0 (FastAPI 0.99.0 and above) supports JSON Schema `examples`; the single `example` keyword is deprecated, so migrate it to `examples`.
- Before 0.103.0 the OpenAPI-specific parameter was named `examples`.

## Verify
Open `/docs` and check the example shown for the body.

## Checked

Read the full tutorial/schema-extra-example.md source page. Confirmed model_config json_schema_extra, Field examples, examples on Path/Query/Header/Cookie/Body/Form/File, the Swagger UI note dated 2023-08-26, openapi_examples (FastAPI 0.103.0) and its summary/description/value/externalValue keys, and the OpenAPI 3.1.0 / FastAPI 0.99.0 notes. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
