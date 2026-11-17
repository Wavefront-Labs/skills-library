---
id: computing-software.web-development.fastapi.query-parameters-defaults
name: query-parameters-defaults
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, defaults, optional-parameters, required-parameters]
level: intro
status: docs-checked
description: "How FastAPI treats function arguments outside the path as query parameters, and how defaults, None and no default decide optional versus required."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query parameters and defaults

Goal: declare optional and required query parameters correctly.

## Rules
- Function parameters that are not part of the path are interpreted as query parameters (the key-value pairs after `?`, separated by `&`).
- Declared types convert and validate them: `skip: int` turns the string `0` into an int.
- A default value makes the parameter optional. With `skip=0` and `limit=10` defaults, `/items/?skip=20` gives `skip=20` and `limit=10`.
- Default `None` makes it optional without a value.
- No default makes it required. A missing required parameter returns an error with `"type": "missing"`, `"loc": ["query", "needy"]` and `"msg": "Field required"`.
- You can mix required, defaulted and optional parameters, and declare them in any order; FastAPI detects them by name and knows which are path parameters.

## Verify
Call the route without the required parameter and expect the `missing` error; then add it and expect success.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
