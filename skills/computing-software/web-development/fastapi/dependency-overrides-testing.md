---
id: computing-software.web-development.fastapi.dependency-overrides-testing
name: dependency-overrides-testing
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, testing, dependency-overrides, mock, dependency-injection]
level: practitioner
status: docs-checked
description: "Replace FastAPI dependencies in tests with app.dependency_overrides, for example to stub an external auth provider, and reset the overrides afterwards."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/testing-dependencies.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overriding dependencies in tests

Goal: keep the original dependency (and its sub-dependencies) from running; supply a stand-in.

## Method
- `app.dependency_overrides` is a plain `dict`: key is the original dependency function, value is the replacement function.
- Typical use: an external authentication provider that costs money or is slow; override with a function returning a mock user.
- It works for a dependency used anywhere: in a path operation function, a decorator `dependencies=` list, an `include_router()` call, etc.
- Reset with `app.dependency_overrides = {}`.
- To limit it to some tests, set the override at the start of the test and reset at the end.

## Verify
Call the endpoint through `TestClient` and assert the response uses the stub value.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there. Removed the claim that settings can be provided through a dependency (not on the cited page).
Method: docs-only read of cited pages, 2026-11-08
