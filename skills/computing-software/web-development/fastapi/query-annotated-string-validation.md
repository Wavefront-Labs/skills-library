---
id: computing-software.web-development.fastapi.query-annotated-string-validation
name: query-annotated-string-validation
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, annotated, query, max-length, min-length, regex-pattern]
level: practitioner
status: docs-checked
description: "Add max_length, min_length and pattern validation to a FastAPI query parameter with Query inside Annotated, and why Annotated beats Query as a default."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params-str-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query() inside Annotated

Goal: validate string query parameters.

## Method
- Import `Query` from `fastapi` and `Annotated` from `typing`.
- Wrap the type: `q: Annotated[str | None, Query(max_length=50)] = None`. The default stays on the function parameter, so `q` is still optional.
- `min_length` and a regular-expression `pattern` work the same way; `^fixedquery$` means start, exact text, end.
- FastAPI validates, returns a clear error, and documents the parameter in OpenAPI.

## Rules
- `Annotated` support arrived (and is recommended) in FastAPI 0.95.0; the docs say to upgrade to at least 0.95.1 first.
- Inside `Annotated` you cannot pass `default` to `Query`: `Annotated[str, Query(default="rick")] = "morty"` is ambiguous. Use `Annotated[str, Query()] = "rick"`.
- Old style `q: str | None = Query(default=None, max_length=50)` still appears in older code. Prefer `Annotated`: the real default is on the parameter, so the function also works when called without FastAPI.
- Any default, including `None`, makes the parameter optional.

## Verify
Send a 51-character `q` and expect a validation error.

## Checked

Read the full tutorial/query-params-str-validations.md source page. Confirmed Query inside Annotated with max_length=50, min_length, pattern ^fixedquery$ meaning, Annotated support from 0.95.0 (upgrade to at least 0.95.1), the rule that Query(default=...) is not allowed inside Annotated, the advantages of Annotated, and that any default makes a parameter optional. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
