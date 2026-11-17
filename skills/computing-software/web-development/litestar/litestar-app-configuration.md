---
id: computing-software.web-development.litestar.litestar-app-configuration
name: litestar-app-configuration
category: computing-software
field: web-development
product: litestar
tags: [litestar, litestar-app, app-config, application-object, layered-architecture, route-handlers, asgi]
level: practitioner
status: docs-checked
description: "Create the root Litestar application object, register handlers on it, and use the four-layer parameter precedence (app, router, controller, handler)."
sources: [https://docs.litestar.dev/latest/usage/applications.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar application object and layered configuration

Goal: build the root `Litestar` instance and know which layer's setting wins.

## Method

- Every app has a `Litestar` instance at its root, usually in `main.py`, `app.py` or `asgi.py` at the project root. These entry points are also what CLI autodiscovery looks for.
- The only required argument is a list of Controllers, Routers or route handlers. The app is the root level with base path `/`; all root-level controllers, routers and handlers register on it.

```python
from litestar import Litestar, get


@get("/")
async def hello_world() -> dict[str, str]:
    """Handler function that returns a greeting dictionary."""
    return {"hello": "world"}


app = Litestar(route_handlers=[hello_world])
```

- Litestar has 4 layers: the application object, Routers, Controllers, Handlers. When a parameter is set on several layers, the one **closest to the handler** takes precedence, so you can override app-wide defaults per handler.
- Parameters that support layering: after_request, after_response, before_request, cache_control, dependencies, dto, etag, exception_handlers, guards, include_in_schema, middleware, opt, request_class, response_class, response_cookies, response_headers, return_dto, security, tags, type_decoders, type_encoders, websocket_class.
- To share configuration between apps, use an `on_app_init` handler that receives and returns `AppConfig` (see the application hooks skill).

## Gotchas

- Setting a layered parameter on the app only supplies a default; any router, controller or handler setting overrides it.

## Verify

Run the hello world app with an ASGI server; the `/` route returns `{"hello": "world"}`.

## Checked

2026-11-07. Read the full cited page(s) (usage/applications.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
