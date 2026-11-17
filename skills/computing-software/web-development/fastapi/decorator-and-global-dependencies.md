---
id: computing-software.web-development.fastapi.decorator-and-global-dependencies
name: decorator-and-global-dependencies
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, dependencies-list, path-operation-decorator, global-dependencies]
level: practitioner
status: docs-checked
description: "Run FastAPI dependencies without using their value by passing dependencies=[Depends(...)] to a path operation decorator or to the FastAPI app."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md, https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/global-dependencies.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependencies that return nothing you need

Goal: enforce a check without an unused parameter.

## Decorator level
- Pass `dependencies=[Depends(...)]` (a list) to the path operation decorator.
- They are solved like normal dependencies, but their return value is not passed to the function.
- Benefits: avoids editors flagging unused parameters, and avoids confusing newcomers.
- They can declare request requirements (the docs use invented `X-Key` and `X-Token` headers), have sub-dependencies, raise exceptions, and return values that are ignored. You can reuse a dependency that returns a value elsewhere.
- For real security prefer the integrated security utilities.

## Application level
Give `dependencies` to the `FastAPI` application and it applies to every path operation. Everything above still applies.

## Groups
A single `dependencies` parameter for a group of path operations is covered in the bigger-applications material (APIRouter).

## Verify
Call a route without the required header and expect the dependency's error.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
