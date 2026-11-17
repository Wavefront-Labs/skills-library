---
id: computing-software.web-development.litestar.litestar-from-fastapi
name: litestar-from-fastapi
category: computing-software
field: web-development
product: litestar
tags: [litestar, fastapi, migration, onboarding, dependency-injection, route-handlers, layered-config, websockets]
level: practitioner
status: docs-checked
description: "Translate FastAPI concepts to Litestar: handler registration, FromPath/FromQuery, data bodies, sync_to_thread, status defaults, Provide, guards, middleware and tests."
sources: [https://docs.litestar.dev/latest/onboarding/fastapi.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from FastAPI to Litestar

Goal: map each FastAPI idiom to its Litestar equivalent.

## Method

- Layers: Application (`Litestar`), then `Router`/`Controller`, then handler. Dependencies, exception handlers, guards, middleware, response cookies/headers, lifecycle hooks and OpenAPI settings can be set on any layer; the value closest to the handler wins.
- Routes: no decorators on app or router. Write `@get("/")` handlers and register with `Litestar([handler])`. A `Router` is not an ASGI app, is flattened at registration and runs no lifecycle hooks (those live on the app). Host-based routing is unsupported: run one app per host behind a reverse proxy.
- Lifespan: `lifespan=[ctx_mgr]`. State: `state: State` in dependencies, `request.app.state` in handlers; `request.state` is per request.
- Parameters are explicit: mark with `FromPath` / `FromQuery` (constraints via `Annotated` `PathParameter` / `QueryParameter`), `FromHeader` / `FromCookie`. Litestar does not auto-match snake case names to header or cookie names; give the name explicitly.
- Bodies: always the `data` parameter. Types: builtins, dataclasses, Pydantic, msgspec `Struct`, attrs. Forms use `data` annotated with `Body(media_type=RequestEncodingType.URL_ENCODED)` or `MULTI_PART`; uploads are `UploadFile` (`list[UploadFile]` for several).
- Sync handlers: threadpool is opt-in. `sync_to_thread=True` to use it; omitting it warns at startup; `False` states you do not want it.
- Responses: POST defaults to 201, DELETE to 204, others 200 (override with `status_code=`). Cookies and headers: `response_cookies` / `response_headers` on the decorator, or return `Response(cookies=..., headers=...)`. Return annotation drives serialization; `media_type=` overrides. Templates: `TemplateConfig` on the app, handlers return `Template`. Streaming: `Stream(iterator)`.
- DI: `dependencies={"name": Provide(fn)}` on any layer; async callables work natively, sync ones need `Provide`.
- No `app.dependency_overrides`. Prefer an app factory taking the dependencies, then a fresh app per test via `create_test_client(..., dependencies=...)`, and mocking last.
- Exceptions: `HTTPException(status_code=400, detail=...)`; a positional argument is appended to `detail`. Handlers: `exception_handlers={Exc: handler}` (class or status code key).
- Auth: a guard (receives `ASGIConnection` and the route handler; raise to abort) or custom authentication middleware.
- Middleware: pure ASGI works unchanged; `BaseHTTPMiddleware` becomes an `ASGIMiddleware` subclass implementing `handle(scope, receive, send, next_app)`.
- Background: `Response(background=BackgroundTask(...))`, run after the body is sent.
- WebSockets: `websocket` (raw), `websocket_listener`, `websocket_stream`; pair with the channels plugin for pub/sub.
- Tests: `TestClient`, `create_test_client`, `create_async_test_client`.
- OpenAPI: per-decorator `tags`, `summary`, `description`, `operation_id`, plus `OpenAPIConfig` via `openapi_config=`.

## Verify

Check your port against the page's quick-reference table, for example POST default status `201` and DELETE `204`.

## Checked

2026-11-07. Read the full cited page(s) (onboarding/fastapi.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
