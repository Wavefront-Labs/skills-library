---
id: computing-software.web-development.fastapi.path-parameters-types
name: path-parameters-types
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, path-parameters, type-hints, validation, int-parsing, pydantic]
level: intro
status: docs-checked
description: "Declare FastAPI path parameters with Python type annotations to get parsing, validation and docs, and read the int_parsing error they return."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/path-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path parameters with types

Goal: turn URL segments into typed Python arguments.

## Method
- Put the variable in the route using Python format-string syntax, for example `/items/{item_id}`, and add a function argument with the same name. The value is passed to that argument.
- Annotate the argument (for example `item_id: int`). FastAPI then converts the string from the URL into that type ("parsing") and validates it. Requesting `/items/3` gives the Python `int` 3, not the string `"3"`.
- A value that does not fit, such as `/items/foo` or a float like `/items/4.2` for an `int`, returns an HTTP error whose `detail` list names the failing spot, e.g. `"type": "int_parsing"` with `"loc": ["path", "item_id"]`.
- Validation is performed by Pydantic, so other types (`str`, `float`, `bool`, and more complex ones) work the same way.
- The same annotation feeds the interactive docs at `/docs` (Swagger UI) and the alternative at `/redoc`, both generated from the OpenAPI schema.

## Gotchas
- The error body tells you exactly where validation failed; use `loc` when debugging clients.

## Verify
Open `/items/3` (expect an integer in the JSON) and `/items/foo` (expect the `int_parsing` error).

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there. Removed the unstated 422 status code from the description.
Method: docs-only read of cited pages, 2026-11-08
