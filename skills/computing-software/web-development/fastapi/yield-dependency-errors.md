---
id: computing-software.web-development.fastapi.yield-dependency-errors
name: yield-dependency-errors
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, yield, exceptions, httpexception, re-raise, logging]
level: advanced
status: docs-checked
description: "Handle exceptions in FastAPI yield dependencies: raise HTTPException from them, never swallow errors with except, and re-raise so the server logs them."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exceptions in yield dependencies

Goal: avoid silent 500 errors.

## Rules
- Exceptions raised in the path operation (including `HTTPException`) are passed into dependencies with `yield`. In most cases re-raise the same or a new exception there so it is handled properly.
- You can catch an exception with `except` and raise a different one, e.g. `HTTPException`. This is advanced and usually unnecessary: you can raise from the path operation code instead.
- If you catch an exception and do not re-raise (or raise a new one), FastAPI cannot see it. The client gets an HTTP 500, but the server has no logs or indication of the cause.
- So unless you raise another `HTTPException` or similar, re-raise the original with a bare `raise`; the client still sees 500 but your error appears in server logs.
- Only one response is ever sent. After the path operation response is sent, it cannot be changed. For a custom response based on an exception, use a custom exception handler.
- Exceptions inside background tasks are handled in the task code, after the response.

## Verify
Force an error inside the route and check the server log shows the original exception.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
