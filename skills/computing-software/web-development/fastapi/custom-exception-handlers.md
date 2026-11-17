---
id: computing-software.web-development.fastapi.custom-exception-handlers
name: custom-exception-handlers
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, error-handling, exception-handler, requestvalidationerror, starlette, httpexception]
level: advanced
status: docs-checked
description: "Register FastAPI exception handlers, override RequestValidationError and HTTPException handling, and register against Starlette's HTTPException."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/handling-errors.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom and overridden exception handlers

Goal: control error responses globally.

## Custom exceptions
Decorate a function with `@app.exception_handler(MyException)`. It receives the `Request` and the exception and returns a response (the docs return a `JSONResponse` with status 418). `fastapi.responses` and `starlette.responses` give the same classes.

## Overriding defaults
- Invalid request data raises `RequestValidationError`; override with `@app.exception_handler(RequestValidationError)`.
- Override the `HTTPException` handler the same way, e.g. to return plain text.
- `RequestValidationError` carries file and line information, so do not return `str(exc)` directly (it can leak system details); extract each error as the docs example does.
- It also holds the received `body`, useful for logging while developing.

## Which HTTPException
FastAPI's `HTTPException` inherits from Starlette's; FastAPI's accepts any JSON-able `detail`, Starlette's only strings. Raise FastAPI's, but register handlers for Starlette's (`from starlette.exceptions import HTTPException as StarletteHTTPException`) so errors raised inside Starlette code are caught too.

## Reuse defaults
Import the default handlers from `fastapi.exception_handlers` to run custom logic and then delegate.

## Verify
Request `/items/foo` and confirm the new error format.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
