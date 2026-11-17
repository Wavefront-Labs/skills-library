---
id: computing-software.web-development.fastapi.lifespan-events
name: lifespan-events
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, lifespan, startup, shutdown, asynccontextmanager, events, sub-applications]
level: practitioner
status: docs-checked
description: "Run FastAPI startup and shutdown logic with a lifespan async context manager, why it replaces startup and shutdown event handlers, and its sub-app limit."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/events.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lifespan events

Goal: set up shared resources once (database pool, ML model) and clean up at shutdown.

## Method
- Write an `async def lifespan(app)` with a single `yield`, decorated with `@asynccontextmanager` (from `contextlib`).
- Code before `yield` runs once before the app takes requests; code after runs after requests finish, at shutdown (release memory, GPU, etc.).
- Pass it: `FastAPI(lifespan=lifespan)`.
- Loading at module level instead would also run during simple automated tests and slow them.

## Deprecated alternative
- `@app.on_event("startup")` and `@app.on_event("shutdown")` handlers (`def` or `async def`).
- If you give `lifespan`, startup and shutdown handlers are no longer called: all lifespan or all events.
- Separate functions make shared state awkward (globals), hence the recommendation of lifespan.

## Notes
- Part of the ASGI Lifespan Protocol (Starlette docs cover lifespan state).
- Lifespan events run only for the main application, not for mounted sub applications.

## Verify
Log a line before and after the `yield`; start and stop the server and check both appear.

## Checked

Confirmed on the cited FastAPI lifespan-events page: lifespan with a single yield and `@asynccontextmanager`, run once before requests and after they finish, `FastAPI(lifespan=...)`, the deprecated startup and shutdown handlers (`def` or `async def`, several allowed), the all-lifespan-or-all-events rule, the module-level loading drawback, the ASGI Lifespan Protocol note and the sub-application limit. Removed: nothing.

Method: docs-only read of cited pages, 2026-11-08
