---
id: computing-software.web-development.fastapi.bigger-applications-apirouter
name: bigger-applications-apirouter
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, apirouter, include-router, bigger-applications, project-structure, relative-imports, router-prefix]
level: practitioner
status: docs-checked
description: "Split a FastAPI app across files with APIRouter and include_router, setting prefix, tags, responses and dependencies on the router or at include time."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/bigger-applications.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigger applications with APIRouter

Goal: structure a multi-file API.

## Method
- Make each directory a package with `__init__.py`; `app/main.py` ties it together, routers live in `app/routers/`.
- In each module create `router = APIRouter()` and declare path operations on it like on `FastAPI`; it is a mini FastAPI with the same parameters.
- Shared settings can go on the router: `prefix` (must not end with `/`), `tags`, `responses`, `dependencies`. Router dependencies run first, then decorator `dependencies`, then parameter dependencies.
- Router dependencies pass no value to the function.
- Import shared code with relative imports: `..dependencies` from `app/routers/items.py` means `app/dependencies.py`.
- In `main.py` import submodules (`from .routers import items, users`) rather than each `router`, which would overwrite the other.
- `app.include_router(users.router)` adds the routes. For a router you cannot modify, pass `prefix`, `tags`, `dependencies`, `responses` to `include_router`; the original stays unchanged.
- You can include the same router several times with different prefixes, and include a router in another with `router.include_router(other)`.
- Do not mutate `router.routes` after including.
- Set `[tool.fastapi] entrypoint = "app.main:app"` in `pyproject.toml` so the `fastapi` command finds the app.

## Verify
Open `/docs` and check paths, prefixes and tags.

## Checked

Method: docs-only read of cited pages, 2026-11-08
