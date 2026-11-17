---
id: computing-software.web-development.fastapi.query-alias-deprecated-hidden
name: query-alias-deprecated-hidden
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, alias, deprecated, include-in-schema, metadata]
level: practitioner
status: docs-checked
description: "Use Query alias, title, description, deprecated and include_in_schema to rename, document, deprecate or hide a FastAPI query parameter."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params-str-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query parameter metadata

Goal: control how a query parameter is named and documented.

## Options on `Query`
- `title` and `description`: extra information included in the generated OpenAPI and shown by docs UIs. Different tools support different amounts of it.
- `alias`: use when the wire name is not a valid Python identifier. For `?item-query=foobaritems`, the closest identifier is `item_query`; declare an alias so the alias is used to find the value.
- `deprecated=True`: keep a parameter that clients still use but show it as deprecated in the docs.
- `include_in_schema=False`: exclude the parameter from the OpenAPI schema and so from the automatic docs.

The same arguments are accepted by `Path`, `Body`, `Header` and `Cookie`.

## Verify
Open `/docs` and check the parameter shows the title, description or deprecated mark, or is absent when excluded.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
