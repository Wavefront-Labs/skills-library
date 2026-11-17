---
id: computing-software.web-development.fastapi.dependency-classes
name: dependency-classes
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, depends, callable, class-dependency, shortcut]
level: practitioner
status: docs-checked
description: "Use a Python class as a FastAPI dependency because any callable works, and use the Depends() shortcut so the class name is not written twice."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/classes-as-dependencies.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classes as dependencies

Goal: get an object with editor support instead of a dict.

## Rules
- A dependency just needs to be a callable (function, class, anything you can call like `something()`). Calling a class creates an instance, so a class qualifies.
- FastAPI analyses the callable's parameters (for a class, its `__init__`) like a path operation function's, including sub-dependencies, conversion, validation and docs.
- Declare `commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]`. The class inside `Depends` is what FastAPI calls; the first one is only a type hint for your editor. `Annotated[Any, Depends(CommonQueryParams)]` works but loses editor help.
- Shortcut when the dependency is the class itself: `commons: Annotated[CommonQueryParams, Depends()]`. The docs say to skip it if it seems more confusing than helpful.
- Non-`Annotated` form (`= Depends(...)`) exists, but prefer `Annotated`.

## Verify
Check the instance type in the route and that query parameters still appear in `/docs`.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
