---
id: computing-software.web-development.litestar.litestar-route-handler-decorators
name: litestar-route-handler-decorators
category: computing-software
field: web-development
product: litestar
tags: [litestar, route-handler, decorators, http-verbs, websocket, asgi, type-annotations, reserved-kwargs]
level: practitioner
status: docs-checked
description: "Define Litestar route handlers with get/post decorators, multiple paths, reserved keyword arguments and the required type annotations."
sources: [https://docs.litestar.dev/latest/usage/routing/handlers.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar route handler decorators

Goal: declare HTTP, websocket and ASGI endpoints by decorating functions or methods.

## Method

- Decorate with a semantic decorator: `@delete`, `@get`, `@head`, `@patch`, `@post`, `@put`. Each pre-sets `http_method`. `@route(path=..., http_method=[HttpMethod.GET, HttpMethod.POST])` is discouraged because OpenAPI treats each verb plus path as a distinct operation that should have its own `operation_id`, `summary` and `description`.
- Path is positional or `path=`; it can be a string or a list of strings. A list allows an optional path parameter:

```python
from litestar import get
from litestar.params import FromPath

@get(["/some-path", "/some-path/{some_id:int}"])
async def my_route_handler(some_id: FromPath[int] = 1) -> None: ...
```

- Handlers can also be built directly: `HTTPRouteHandler(path="/some-path", http_method=[...], fn=my_endpoint)`.
- Reserved keyword arguments, each declared with its type: `cookies: RequestCookies`, `headers: Headers`, `query: QueryParams`, `request: Request` (HTTP handlers only), `scope: Scope`, `socket: WebSocket` (websocket handlers only), `state: State`, `body: RawBody` (HTTP only), and `data` (parsed body, declared with a marker such as `JSONBody`). Path, query, header and cookie values use `FromPath`, `FromQuery`, `FromHeader`, `FromCookie`. If a parameter name collides with a reserved one, give it an alternative name via aliasing.
- Websocket: `@websocket(path="/socket")` must declare a `socket` kwarg, return `None`, and be `async`. No OpenAPI schema is generated for it.
- ASGI: `@asgi(path=...)` takes exactly `scope`, `receive`, `send`, and must be `async`. The scope is a copy; pass `copy_scope=False` if the wrapped app must communicate with the outer app through the scope.

## Gotchas

- All arguments and the return value must be type annotated; a missing annotation raises `ImproperlyConfiguredException` at application boot-up.
- Violating the websocket or ASGI requirements raises an informative exception from inspection.

## Verify

Start the app: a missing annotation fails at boot-up with `ImproperlyConfiguredException`, as the page states.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/handlers.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
