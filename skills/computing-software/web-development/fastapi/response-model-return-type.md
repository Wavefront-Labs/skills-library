---
id: computing-software.web-development.fastapi.response-model-return-type
name: response-model-return-type
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, response-model, return-type, filtering, pydantic, security, output-model]
level: practitioner
status: docs-checked
description: "Choose between a return type annotation and the response_model decorator parameter in FastAPI to validate, filter and document output such as hiding passwords."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/response-model.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Return type vs response_model

Goal: control what leaves the API.

## What FastAPI does with it
Validates the returned data (a missing field is a server error, not bad data), adds a JSON Schema to OpenAPI, serializes with Pydantic, and filters output to the declared fields (important for security).

## Choosing
- Annotate the function return type when you return what you declare.
- Use the decorator parameter `response_model` (on `get`, `post`, `put`, `delete`, not the function) when you return a dict or database object but want a Pydantic model applied. If both exist, `response_model` wins. Declaring the return type `Any` keeps strict type checkers quiet.
- Different input and output models (input with plaintext password, `UserOut` without) means FastAPI filters out undeclared fields.
- Keep tooling happy and still filter: annotate the base class (`BaseUser`) and return a subclass (`UserIn`); FastAPI filters to the declared type and does not use inheritance to leak extra fields.

## Gotchas
- `EmailStr` needs `email-validator` (e.g. `pydantic[email]`).
- Returning a `Response` or subclass annotated as such is handled automatically. A union of `Response` and `dict`, or any non-Pydantic type, makes FastAPI fail building a model; set `response_model=None` to disable it.

## Checked

Method: docs-only read of cited pages, 2026-11-08
