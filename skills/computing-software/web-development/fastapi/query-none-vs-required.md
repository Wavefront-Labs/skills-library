---
id: computing-software.web-development.fastapi.query-none-vs-required
name: query-none-vs-required
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, required-parameters, none, optional-type]
level: practitioner
status: docs-checked
description: "Why a FastAPI query parameter typed str | None without a default is still required, and why ?q=None or ?q=null never produce a Python None."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params-str-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Required versus nullable query parameters

Goal: avoid confusing "may be None" with "may be omitted".

## Rules
- To make a parameter required, declare no default: `q: str`, or `Annotated[str, Query(min_length=3)]` with no `= ...` default.
- `str | None` allows `None` as a Python value but does not make the query parameter optional. With no default it is still required.
- Query values arrive as strings with no built-in `None`: `?q=None` sends the string `"None"`, `?q=null` sends `"null"`, and `?q=` sends an empty string (which fails `min_length=3`).
- To let clients omit it, give a default: `q: Annotated[str | None, Query(min_length=3)] = None`.
- JSON request bodies, unlike query strings, can carry an explicit `null`.

## Checked

Method: docs-only read of cited pages, 2026-11-08
