---
id: computing-software.web-development.litestar.litestar-from-flask
name: litestar-from-flask
category: computing-software
field: web-development
product: litestar
tags: [litestar, flask, migration, onboarding, request, sessions, hooks, path-parameters]
level: practitioner
status: docs-checked
description: "Translate Flask concepts to Litestar: path parameters, request access, g and current_app, status codes, templates, errorhandler, hooks, sessions and tests."
sources: [https://docs.litestar.dev/latest/onboarding/flask.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from Flask to Litestar

Goal: map Flask idioms to Litestar equivalents.

## Method

- Layers: Application, then `Router`/`Controller`, then handler. Dependencies, exception handlers, guards, middleware, response cookies/headers, lifecycle hooks and OpenAPI settings merge across layers; the setting closest to the handler wins.
- Routes: `@app.route("/")` becomes `@get("/")` registered with `Litestar([handler])`.
- Path parameters: `/post/<int:post_id>` becomes `/post/{post_id:int}`, requested with `FromPath` (name matches by default, aliasing possible). The path type defines input and OpenAPI; the function annotation is what is validated.
- Sync vs async: Litestar is ASGI, asynchronous throughout. Run blocking sync handlers off the event loop with `@get("/", sync_to_thread=True)`. A sync handler without `sync_to_thread` emits a runtime warning; pass `sync_to_thread=False` when the body does not block.
- Lifespan: `lifespan=[ctx_mgr]`, setup before `yield`, teardown after (Flask has no shutdown hook).
- Request: take `request: Request` as a parameter instead of the global. Table highlights: `request.args` becomes `FromQuery` parameters or `request.query_params`; `request.data` becomes `await request.body()`; `request.form` / `get_json` become the `data` parameter; `request.files` becomes `UploadFile`; `request.authorization` becomes `request.auth`; `request.endpoint` becomes `request.route_handler.name`; `request.environ` becomes `request.scope`; `request.remote_addr` becomes `request.client.host`; `request.path` becomes `request.scope["path"]`; other headers via `request.headers.get("...")`.
- `flask.g` becomes `request.state`; `current_app` becomes `request.app` (or an `app` parameter on lifecycle hooks and middleware factories).
- Uploads: `data` typed `UploadFile` (or a list) with `Body` media type `MULTI_PART` or `URL_ENCODED`.
- Status: `return body, 404` becomes `status_code=` on the decorator, or on the `Response` when request dependent. Defaults: POST 201, DELETE 204, others 200.
- Cookies/headers: `response_cookies` and `response_headers` on the decorator, or `Response(cookies=..., headers=...)`.
- Serialization comes from the return annotation: structured types to JSON, `str` to `text/plain`; override with `media_type=`.
- URL lookup: `url_for` becomes `request.url_for(name)` where `name=` is set on the decorator.
- Templates: `litestar[jinja]` or `litestar[mako]` extra, `TemplateConfig` on the app, handlers return `Template`.
- Streaming: `Stream(iterator)`.
- Errors: `abort(400, ...)` becomes `raise HTTPException(status_code=400, ...)`; `@app.errorhandler` becomes `exception_handlers={Exc: handler}` (class or status code).
- Hooks: `before_request=` / `after_request=` keywords on any layer.
- Sessions: `request.session` with `ServerSideSessionConfig` (data on the server, id in cookie) or `CookieBackendConfig` (encrypted cookie, closest to Flask).
- Static files: no automatic `static/`; use `create_static_files_router`.
- WebSockets are native: `websocket`, `websocket_listener`, `websocket_stream`; use the channels plugin for pub/sub.
- Tests: `TestClient` (wraps an app) and `create_test_client` (builds an app from `Litestar` options).

## Verify

Cross-check against the page's quick-reference table, for example `flask.g` to `request.state`.

## Checked

2026-11-07. Read the full cited page(s) (onboarding/flask.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
