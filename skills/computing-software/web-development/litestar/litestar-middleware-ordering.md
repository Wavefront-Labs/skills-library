---
id: computing-software.web-development.litestar.litestar-middleware-ordering
name: litestar-middleware-ordering
category: computing-software
field: web-development
product: litestar
tags: [litestar, middleware, call-order, layers, asgi, exceptions]
level: practitioner
status: docs-checked
description: "Attach middleware to Litestar app, router, controller and handler layers, know the call order, and know which exceptions bypass middleware."
sources: [https://docs.litestar.dev/latest/usage/middleware/using-middleware.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar: attaching middleware and call order

Goal: add middleware at the right layer and predict the order it runs in.

## Method

A middleware is any callable that receives a kwarg named `app` (the next ASGI app, not the Litestar instance) and returns an `ASGIApp`:

```python
from litestar import Litestar
from litestar.types import ASGIApp, Scope, Receive, Send

def middleware_factory(app: ASGIApp) -> ASGIApp:
    async def my_middleware(scope: Scope, receive: Receive, send: Send) -> None:
        # do something here
        await app(scope, receive, send)
    return my_middleware

app = Litestar(route_handlers=[...], middleware=[middleware_factory])
```

Middleware is part of the layered architecture: the `middleware` list can be set on the app, router, controller and handler.

Call order: the stack is built in application > handler order, and that is the order middleware is called in. The page's example registers middleware ids 0 and 1 on the app, 2 and 3 on the `Router`, 4 and 5 on the `Controller`, and 6 and 7 on the handler (`middleware=[...]` on `@get`); requesting `/router/controller/handler` records them in numeric order. Within one list, the first entry is the outer wrapper (first to see the request, last to see the response).

## Gotchas

- Exceptions raised by a handler or dependency become responses through an exception handler, and middleware still applies to that response.
- Exception: `NotFoundException` and `MethodNotAllowedException` raised by Litestar's ASGI router occur before the middleware stack is called. Only exception handlers defined on the `Litestar` instance itself handle them, so change those responses with an application-layer exception handler.

## Verify

Using the page's call-order example (each middleware appends its id to `app.state["middleware_calls"]`), request `/router/controller/handler`; the handler returns the list of ids in call order.

## Checked

2026-11-07. Read the full cited page(s) (usage/middleware/using-middleware.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
