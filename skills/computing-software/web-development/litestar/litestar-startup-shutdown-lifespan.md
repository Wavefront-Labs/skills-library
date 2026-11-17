---
id: computing-software.web-development.litestar.litestar-startup-shutdown-lifespan
name: litestar-startup-shutdown-lifespan
category: computing-software
field: web-development
product: litestar
tags: [litestar, lifespan, startup, shutdown, on-startup, on-shutdown, context-manager, asgi]
level: practitioner
status: docs-checked
description: "Run code at Litestar startup and shutdown with on_startup, on_shutdown and async lifespan context managers, including shutdown execution order."
sources: [https://docs.litestar.dev/latest/usage/applications.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar startup, shutdown and lifespan

Goal: open and close resources such as a database connection with the app lifecycle.

## Method

- Pass lists of callables (sync or async functions, methods or class instances) to `on_startup` / `on_shutdown`. They are called in order when the ASGI server (uvicorn, Hypercorn, Granian, Daphne) emits `lifespan.startup` / `lifespan.shutdown`.
- A callable may take an optional `app` argument to reach `app.state`.

```python
def get_db_connection(app: Litestar) -> AsyncEngine:
    if not getattr(app.state, "engine", None):
        app.state.engine = create_async_engine(DB_URI)
    return cast("AsyncEngine", app.state.engine)


async def close_db_connection(app: Litestar) -> None:
    if getattr(app.state, "engine", None):
        await cast("AsyncEngine", app.state.engine).dispose()


app = Litestar(on_startup=[get_db_connection], on_shutdown=[close_db_connection])
```

- For long-running tasks or a context object that must stay alive, use the `lifespan` parameter with an async context manager:

```python
@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine("postgresql+asyncpg://user:password@host:5432/db")
        app.state.engine = engine
    try:
        yield
    finally:
        await engine.dispose()


app = Litestar(lifespan=[db_connection])
```

## Order of execution

With `Litestar(lifespan=[ctx_a, ctx_b], on_shutdown=[hook_a, hook_b])`, shutdown runs: ctx_b, ctx_a, hook_a, hook_b. Context managers exit in inverse order, and all of them before the shutdown hooks; shutdown hooks keep their listed order.

## Verify

Start the app under an ASGI server and stop it; the startup callable runs on lifespan.startup and the cleanup (e.g. engine dispose) on lifespan.shutdown, in the order above.

## Checked

2026-11-07. Read the full cited page(s) (usage/applications.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
