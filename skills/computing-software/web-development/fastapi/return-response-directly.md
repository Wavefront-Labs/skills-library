---
id: computing-software.web-development.fastapi.return-response-directly
name: return-response-directly
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, response, jsonresponse, return-response, jsonable-encoder, performance, xml]
level: practitioner
status: docs-checked
description: "Return a Response or JSONResponse directly from FastAPI, what you give up (validation, conversion, docs), and why a response model is usually faster."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/response-directly.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Return a Response directly

## Rules
- Any `Response` (including `JSONResponse`) you return is passed through untouched: no Pydantic conversion, no validation, no automatic docs. You gain flexibility and take responsibility for correct, serializable data.
- A Pydantic model cannot go straight into a `JSONResponse`. Convert with `jsonable_encoder` first (it turns `datetime`, `UUID` and so on into JSON-compatible types).
- Custom formats: put e.g. XML content in a string, put that in a `Response` and return it.
- Without a response model FastAPI uses `jsonable_encoder` plus `JSONResponse`.
- With a `response_model` or return type, Pydantic serializes to JSON bytes (in Rust) and FastAPI returns a `Response` with `application/json` directly, skipping `jsonable_encoder` and `JSONResponse`; the docs say this is much faster.
- A direct response can still be documented with `responses` (Additional Responses in OpenAPI).

## Checked

Method: docs-only read of cited pages, 2026-11-08
