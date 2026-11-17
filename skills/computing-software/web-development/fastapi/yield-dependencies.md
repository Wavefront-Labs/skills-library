---
id: computing-software.web-development.fastapi.yield-dependencies
name: yield-dependencies
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, yield, cleanup, database-session, context-manager]
level: practitioner
status: docs-checked
description: "Write FastAPI dependencies that clean up after the response using yield, with try/finally, sub-dependency exit order and context managers."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies with yield

Goal: run teardown code such as closing a database session.

## Rules
- Use `yield` once per dependency instead of `return`; code after it is the exit code. Anything valid with `@contextlib.contextmanager` or `asynccontextmanager` is a valid dependency (FastAPI uses them internally; you should not apply them yourself).
- Only the code up to and including `yield` runs before the response is created; the yielded value is injected. Exit code runs after the response.
- Wrap in `try`/`finally` so cleanup runs whether or not an exception occurred; with `except SomeException` you can see exceptions raised in other dependencies or the path operation.
- Sub-dependencies can all use `yield`; FastAPI runs exit code in the correct order (c needs b needs a to still be available).
- Combine with plain `return` dependencies freely.
- You can use `with` / `async with` inside the dependency for context managers (classes with `__enter__()` and `__exit__()`).
- For versions history see the advanced-dependencies page.

## Verify
Log in the exit section and confirm it prints after the response is sent.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
