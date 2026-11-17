---
id: computing-software.web-development.fastapi.dependency-injection-basics
name: dependency-injection-basics
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, depends, annotated, type-alias, shared-logic]
level: practitioner
status: docs-checked
description: "Write a FastAPI dependency as a plain function, inject it with Depends, share Annotated dependency aliases, and know async/def and OpenAPI behaviour."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/index.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies with Depends

Goal: share logic, connections or security checks across path operations.

## Method
- A dependency is a function taking the same kind of parameters as a path operation function (query parameters like `q`, `skip`, `limit`) and returning anything.
- Import `Depends` from `fastapi` and add a parameter such as `commons: Annotated[dict, Depends(common_parameters)]`.
- `Depends` takes a single argument, a callable. Do not call it: no parentheses at the end.
- Per request FastAPI calls the dependency with the right arguments, then assigns the result to your parameter. You do not register it anywhere.
- To avoid repeating the annotation, store the `Annotated[...]` value in a variable (a standard Python type alias); type information and autocompletion are preserved.
- `async def` and `def` can be mixed freely, in dependencies and path operations.
- A dependency's parameters and validation are added to the OpenAPI schema and docs.
- `Annotated` requires FastAPI 0.95.1 or later per the docs.

## Common uses
Shared logic, shared database connections, authentication and role requirements.

## Verify
Open `/docs` and confirm the dependency's query parameters appear on each route using it.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
