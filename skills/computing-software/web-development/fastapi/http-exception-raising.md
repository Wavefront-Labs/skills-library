---
id: computing-software.web-development.fastapi.http-exception-raising
name: http-exception-raising
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, error-handling, httpexception, status-code, custom-headers, detail]
level: intro
status: docs-checked
description: "Return client errors from FastAPI by raising HTTPException with a status code, a JSON-able detail and optional custom headers."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/handling-errors.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raising HTTPException

Goal: send a 4xx response from anywhere in a request.

## Rules
- Client errors use status codes 400 to 499 (for example 404 not found); 200 to 299 mean success.
- Import `HTTPException` from `fastapi`. It is a normal Python exception, so you `raise` it, you do not `return` it.
- Raising inside a helper called by the path operation stops the rest of the path operation and sends the error to the client at once.
- Typical use: raise with `status_code=404` and `detail="Item not found"`; the client receives `{"detail": "Item not found"}`.
- `detail` can be any JSON-convertible value (a `dict`, a `list`), not only a `str`.
- Custom headers on the error are possible for advanced cases such as some security schemes.

## Verify
Request a missing resource and check both the status code and the `detail` body.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
