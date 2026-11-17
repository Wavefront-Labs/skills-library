---
id: computing-software.web-development.litestar.litestar-handler-metadata-indexing
name: litestar-handler-metadata-indexing
category: computing-software
field: web-development
product: litestar
tags: [litestar, route-handler, route-reverse, handler-name, opt, signature-namespace, metadata, url-for]
level: practitioner
status: docs-checked
description: "Name Litestar handlers for route_reverse lookups, attach opt metadata at any layer, and resolve runtime types with signature_types."
sources: [https://docs.litestar.dev/latest/usage/routing/handlers.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar handler indexing, opt metadata and signature namespace

Goal: look up handlers and paths by name, attach metadata, and keep type-only imports working.

## Method

Indexing by name:
- Pass `name=` to any handler decorator. It must be unique or `ImproperlyConfiguredException` is raised. The default is the handler's `__str__`, normally its full dotted path (for example `app.controllers.projects.list`).
- `request.app.get_handler_index_by_name(name)` returns a mapping with `paths`, `handler` and `qualname`.
- `app.route_reverse("three", param=5)` builds a path; a handler reference also works: `app.route_reverse(handler_one)  # Returns "/abc"`.
- With several paths on one handler, `route_reverse` returns the path that consumes the most keyword arguments:

```python
@get(["/some-path", "/some-path/{id:int}", "/some-path/{id:int}/{val:str}"], name="handler_name")
def handler(id: FromPath[int] = 1, val: FromPath[str] = "default") -> None: ...
# route_reverse("handler_name") -> /some-path
# route_reverse("handler_name", id=100) -> /some-path/100
```

- With a `Request`, `request.url_for(...)` (`ASGIConnection.url_for`) returns an absolute URL.

Metadata:
- `@get("/", opt={"my_key": "some-value"})`, or pass any extra kwarg (`my_key="some-value"`) and it lands in `handler.opt`.
- Read it in guards, via `request.route_handler`, or from the ASGI scope.
- `opt` can be set on handlers, controllers, routers and the app; dicts merge and the layer closest to the handler wins.

Signature namespace:
- Litestar builds a signature model from runtime types. Types imported only under `if TYPE_CHECKING:` are unavailable, so pass `signature_types` (any layer) or `signature_namespace={"FooModel": Model}` (for example on `Litestar(...)`).
- Already available by default: `Headers`, `ImmutableState`, `Receive`, `Request`, `Scope`, `Send`, `State`, `WebSocket`, `WebSocketScope`.

## Gotchas

- `route_reverse` raises `NoRouteMatchFoundException` for an unknown name or missing/mistyped path parameters; `str` is accepted for datetime, date, time, timedelta, float and Path parameters.
- A handler registered on several routes with identical path parameters gives unpredictable results; avoid reversing it.

## Verify

`assert handler.opt["my_key"] == "some-value"` after `@get("/", my_key="some-value")`, as the page shows.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/handlers.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
