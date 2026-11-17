---
id: computing-software.web-development.fastapi.additional-responses-openapi
name: additional-responses-openapi
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, responses, openapi, additional-responses, media-type, response-model, status-code]
level: advanced
status: docs-checked
description: "Document extra FastAPI responses with the responses parameter: extra status codes with models, extra media types, merging with response_model and reusing dicts."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/additional-responses.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Additional responses in OpenAPI

## Method
- Pass `responses={status_code: {...}}` on the decorator. Each value may hold `model` (a Pydantic model; FastAPI builds the JSON Schema and references it under `content` / media type / `schema`), plus OpenAPI fields such as `description`, `headers`, `content`, `links`.
- `model` is a FastAPI convenience, not part of OpenAPI.
- This only documents. You must return a `Response` such as `JSONResponse` with that status and content yourself.
- Extra media types: add e.g. `"content": {"image/png": {}}` under the main status code, and return a `FileResponse` for the image. Unless stated, FastAPI assumes the main response class media type (default `application/json`); with a custom class whose media type is `None`, extra responses that have a model use `application/json`.
- Combining: a `response_model` plus `responses` is merged. E.g. 404 with a model and custom `description`, and 200 using `response_model` with a custom `example`.
- Reuse predefined responses by unpacking: `responses={**base_responses, 200: {...}}`.
- FastAPI also adds the default 200 and 422 (HTTPValidationError) entries.

## Verify
Check the response list for the operation in `/docs`.

## Checked

Method: docs-only read of cited pages, 2026-11-08
