---
id: computing-software.web-development.litestar.litestar-routing-registration
name: litestar-routing-registration
category: computing-software
field: web-development
product: litestar
tags: [litestar, routing, register, route-handlers, dynamic-routes, multiple-paths, radix-tree]
level: practitioner
status: docs-checked
description: "Register Litestar route handlers on the app, give one handler several paths, add routes dynamically with register, and reuse handlers on several routers."
sources: [https://docs.litestar.dev/latest/usage/routing/overview.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar registering routes

Goal: attach handlers, routers and controllers to the app, statically or dynamically.

## Method

- Root-level controllers, routers and handlers register through the `route_handlers` argument of `Litestar`. Components are appended to the root path.

```python
@get("/sub-path")
def sub_path_handler() -> None: ...


@get()
def root_handler() -> None: ...


app = Litestar(route_handlers=[root_handler, sub_path_handler])
```

Here `root_handler` serves `/` and `sub_path_handler` serves `/sub-path`.

- One handler, several paths: `@get(["/", "/sub-path"])`.
- Dynamic registration: `app.register(sub_path_handler)` after the app is created. The app is attached to every connection, so `request.app.register(...)` works inside handlers, middleware and dependencies:

```python
@get("/some-path")
def route_handler(request: Request[Any, Any]) -> None:
    @get("/sub-path")
    def sub_path_handler() -> None: ...

    request.app.register(sub_path_handler)
```

- Registering a handler or a controller class on several routers is allowed. A router creates its own controller instance from the class; a registered handler is copied. So `Router(path="/internal", route_handlers=[my_route_handler])`, `/partner` and `/consumer` expose `/internal/handler`, `/partner/handler`, `/consumer/handler`.

## Gotchas

- Dynamic registration increases complexity; use it only when absolutely required.
- A router that has been registered once cannot be re-registered; an exception is raised.
- For complex path schemas use controllers and routers.
- Litestar routes with a radix tree (trie): the page says this approach is agnostic to the number of routes (better horizontal scaling), at the expense of somewhat slower path parameter resolution than regex routing.

## Verify

With the first example, requests to `/` and `/sub-path` reach `root_handler` and `sub_path_handler` respectively.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/overview.html) and the example files they include, and confirmed the claims in this skill against that text. Reworded the radix-tree note to the page's own claim (agnostic to route count).

Method: documentation only; no commands were run.
