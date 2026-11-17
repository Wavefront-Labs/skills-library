---
id: computing-software.web-development.fastapi.yield-dependency-scope
name: yield-dependency-scope
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, yield, scope, depends-scope, early-exit]
level: advanced
status: docs-checked
description: "Close a FastAPI yield dependency before the response is sent with Depends(scope=\"function\") and know the sub-dependency scope rules."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/dependencies-with-yield.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency scope

Goal: release a resource as soon as the path operation function returns.

## Rules
- Normally the exit code of a `yield` dependency runs after the response is sent to the client.
- `Depends(scope="function")` ends the dependency after the path operation function returns but before the response is sent.
- `scope` values: `"function"` wraps the path operation function; `"request"` wraps the whole request and response cycle.
- A yield dependency with no explicit scope defaults to `"request"`.
- Sub-dependency rule: a `"request"` dependency may only have `"request"` sub-dependencies. A `"function"` dependency can have both `"function"` and `"request"` sub-dependencies, because a dependency must run its exit code before its sub-dependencies close.

## Use when
You know the dependency is not needed after the function returns.

## Verify
Log in the exit code and compare ordering against the response being delivered.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
