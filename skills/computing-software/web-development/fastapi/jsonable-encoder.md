---
id: computing-software.web-development.fastapi.jsonable-encoder
name: jsonable-encoder
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, jsonable-encoder, serialization, pydantic, json, datetime]
level: intro
status: docs-checked
description: "Use jsonable_encoder to turn Pydantic models and datetimes into JSON-compatible dicts and strings before storing them, for example in a database."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/encoder.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON compatible encoder

Goal: convert data to JSON-compatible Python structures.

## Method
- `from fastapi.encoders import jsonable_encoder`; pass it an object such as a Pydantic model.
- A Pydantic model becomes a `dict`; a `datetime` becomes a `str` in ISO format.
- The result is a Python structure (e.g. a `dict`) whose values are all JSON compatible, ready for the standard `json.dumps()`. It does not return a big JSON string.
- Typical use: a store that accepts only JSON-compatible data (no `datetime`, no model objects).
- FastAPI uses it internally to convert data, and it is useful in other scenarios too.

## Verify
`json.dumps(jsonable_encoder(obj))` succeeds.

## Checked

Confirmed on the cited FastAPI JSON compatible encoder page: Pydantic model to `dict`, `datetime` to ISO `str`, the result being a Python structure rather than a JSON string, use with `json.dumps()`, the JSON-only datastore use case and internal use by FastAPI. Removed (not on the page): the testing-guide `TestClient` suggestion.

Method: docs-only read of cited pages, 2026-11-08
