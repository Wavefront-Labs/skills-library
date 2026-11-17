---
id: computing-software.web-development.litestar.litestar-asgi-middleware-authoring
name: litestar-asgi-middleware-authoring
category: computing-software
field: web-development
product: litestar
tags: [litestar, middleware, asgimiddleware, asgi, scopes, exclude-path-pattern, constraints, definemiddleware]
level: practitioner
status: docs-checked
description: "Write Litestar middleware by subclassing ASGIMiddleware: handle(), scopes, path and opt-key exclusion, constraints, and DefineMiddleware arguments."
sources: [https://docs.litestar.dev/latest/usage/middleware/creating-middleware.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar: authoring ASGIMiddleware

Goal: build a reusable middleware class that can skip scopes and paths and declare ordering constraints. `ASGIMiddleware` was introduced in Litestar 2.15 and is the recommended base.

## Method

Subclass `litestar.middleware.ASGIMiddleware` and implement `handle`. It has no `__init__`, so define your own for configuration:

```python
import time
from litestar.datastructures import MutableScopeHeaders
from litestar.enums import ScopeType
from litestar.middleware import ASGIMiddleware
from litestar.types import ASGIApp, Message, Receive, Scope, Send

class ProcessTimeHeader(ASGIMiddleware):
    scopes = (ScopeType.HTTP,)
    exclude_path_pattern = ("first_path", "second_path")
    exclude_opt_key = "exclude_from_my_middleware"

    async def handle(self, scope: Scope, receive: Receive, send: Send, next_app: ASGIApp) -> None:
        start_time = time.monotonic()
        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableScopeHeaders.from_message(message=message)
                headers["X-Process-Time"] = str(time.monotonic() - start_time)
            await send(message)
        await next_app(scope, receive, send_wrapper)

app = Litestar(route_handlers=[...], middleware=[ProcessTimeHeader()])
```

- Modify responses by wrapping `send`; modify requests by wrapping `receive`.
- Skip by `scope["type"]` (`scopes`), by regex path patterns (`exclude_path_pattern`), or per handler by setting the `exclude_opt_key` as a handler opt (`@get(..., exclude_from_my_middleware=True)`).
- Constraints are validated at startup: `constraints = MiddlewareConstraints(after=(AbstractAuthenticationMiddleware,))` from `litestar.middleware.constraints`. Order constraints are `before`, `after`, `first`, `last`; `first=True` means first on the application layer, `last=True` last on the handler layer. String forward refs: `MiddlewareConstraints().apply_after("pkg.mod.SomeMiddleware", ignore_import_error=True)`.
- Plugin-added middleware is placed after app-level and before other layers; with `first=True` use `app_config.middleware.insert(0, MyCustomMiddleware())`.
- Functions or factories with arguments: `middleware=[DefineMiddleware(middleware_factory, 1, my_kwarg="abc")]`.

## Gotchas

- Using `/` as an exclude pattern disables the middleware everywhere, since as a regex it matches every path.
- If you modify request data, modify the `scope`, not an ephemeral `Request`.

## Verify

Per the page's example, a handler matching an exclude pattern or opt key does not get the `X-Process-Time` header; other HTTP routes do.

## Checked

2026-11-07. Read the full cited page(s) (usage/middleware/creating-middleware.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
