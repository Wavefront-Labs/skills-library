---
id: computing-software.web-development.fastapi.response-status-code-declaration
name: response-status-code-declaration
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, status-code, http-status, fastapi-status, path-operation, openapi]
level: intro
status: docs-checked
description: "Set the default HTTP status code of a FastAPI path operation with the decorator status_code parameter, fastapi.status names, and codes that carry no body."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/response-status-code.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Declaring the response status code

Goal: return the right success code and document it.

## Rules
- `status_code` is a parameter of the decorator (`@app.get()`, `@app.post()`, and so on), not of the function. It takes a number, or an `IntEnum` such as `http.HTTPStatus`.
- FastAPI returns that code and documents it in OpenAPI.
- Convenience names live in `fastapi.status` (same numbers; it is `starlette.status`) so autocomplete can help.

## Code ranges
- 100 to 199 information: no body.
- 200 to 299 success: 200 is the default; 201 Created (after creating a record); 204 No Content, which must have no body.
- 300 to 399 redirection: may have a body, except 304 Not Modified.
- 400 to 499 client error: 404 Not Found; 400 for generic client errors.
- 500 to 599 server error: raised automatically when code breaks.

FastAPI knows which codes have no body and documents that.

The Advanced User Guide covers returning a different status code than the declared default.

## Verify
Call the route and inspect the status line; check `/docs` shows the code.

## Checked

Method: docs-only read of cited pages, 2026-11-08
