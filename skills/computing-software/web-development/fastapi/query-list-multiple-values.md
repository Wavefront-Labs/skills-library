---
id: computing-software.web-development.fastapi.query-list-multiple-values
name: query-list-multiple-values
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, query-parameters, list, repeated-parameters, query]
level: practitioner
status: docs-checked
description: "Receive repeated query parameters such as ?q=foo&q=bar as a Python list in FastAPI, with a default list, and why plain list skips item checks."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/query-params-str-validations.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple values for one query parameter

Goal: accept `?q=foo&q=bar` as a list.

## Method
- Declare the parameter with `Query` explicitly and a list type, e.g. `list[str]` inside `Annotated`. The URL `http://localhost:8000/items/?q=foo&q=bar` then gives `["foo", "bar"]`.
- Without explicit `Query`, a `list` type would be interpreted as a request body.
- A default list is allowed (the docs use `["foo", "bar"]`); with no `q` in the URL that default is used.
- You can use plain `list` instead of `list[str]`, but FastAPI then does not check the contents: `list[int]` would check and document that items are integers, `list` would not.
- The interactive docs update to allow multiple values.

## Verify
Request with two `q` values and confirm the JSON shows a list of two items.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
