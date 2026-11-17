---
id: computing-software.web-development.fastapi.sub-dependencies-cache
name: sub-dependencies-cache
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, dependency-injection, sub-dependencies, use-cache, dependency-tree]
level: practitioner
status: docs-checked
description: "Chain FastAPI dependencies into sub-dependency trees, understand the once-per-request cache, and disable it with Depends(use_cache=False)."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/sub-dependencies.md, https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/dependencies/index.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sub-dependencies

Goal: layer dependencies without wiring them manually.

## Rules
- A dependency can itself declare dependencies (it is "dependable" and "dependant"), to any depth. In the docs example, `query_or_cookie_extractor` depends on `query_extractor` and also reads an optional `last_query` cookie.
- The path operation declares only the top dependency. FastAPI solves `query_extractor` first and passes its result along.
- If several dependencies in one path operation share a sub-dependency, it is called only once per request; the value is cached and given to every dependant.
- For the rare case where it must run at every step of the same request, pass `use_cache=False`: `Depends(get_value, use_cache=False)`.

## Why it matters
Permission levels such as current user, active user, admin or paying user can be composed from nested dependencies, each requirement also landing in the OpenAPI schema.

## Verify
Add a print in a shared sub-dependency and confirm it runs once per request.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there. Added the dependencies index page as a source for the permission-levels paragraph.
Method: docs-only read of cited pages, 2026-11-08
