---
id: computing-software.web-development.litestar.litestar-security-guards
name: litestar-security-guards
category: computing-software
field: web-development
product: litestar
tags: [litestar, security, guards, authorization, opt, permission-denied, layers]
level: practitioner
status: docs-checked
description: "Write Litestar guard functions that authorize requests, declare them on app, router, controller or handler layers, and read route handler opt values."
sources: [https://docs.litestar.dev/latest/usage/security/guards.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar guards

Goal: authorize requests before they reach a handler.

## Method

A guard is a callable taking `connection` (a `Request` or `WebSocket`, both `ASGIConnection`) and `route_handler` (a copy of the `BaseRouteHandler`). To deny, raise an `HTTPException`, usually `PermissionDeniedException` (status 403).

```python
from litestar import post
from litestar.connection import ASGIConnection
from litestar.exceptions import PermissionDeniedException
from litestar.handlers.base import BaseRouteHandler

def admin_user_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    if not connection.user.is_admin:
        raise PermissionDeniedException()

@post(path="/user", guards=[admin_user_guard], sync_to_thread=False)
def create_user(data: JSONBody[User]) -> User: ...
```

`connection.user` is populated by the authentication middleware (for example the JWT backend's `retrieve_user_handler`).

Layers: `guards` is a list and can be set on the `Litestar` app, `Router`, `Controller`, or handler:

```python
class UserController(Controller):
    path = "/user"
    guards = [my_guard]

admin_router = Router(path="admin", route_handlers=[UserController], guards=[my_guard])
app = Litestar(route_handlers=[admin_router], guards=[my_guard])
```

Unlike dependencies, guards do not override each other; they are cumulative across layers.

Route handler `opt`: set arbitrary values on a handler with `opt={...}` and read them in the guard through `route_handler.opt`:

```python
def secret_token_guard(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None:
    if (route_handler.opt.get("secret")
            and not connection.headers.get("Secret-Header", "") == route_handler.opt["secret"]):
        raise PermissionDeniedException()

@get(path="/secret", guards=[secret_token_guard], opt={"secret": environ.get("SECRET")})
def secret_endpoint() -> None: ...
```

## Gotchas

- Guards placed at the controller or app level also run on all `OPTIONS` requests (see Litestar issue 2314 for the workaround).

## Checked

2026-11-07. Read the full cited page(s) (usage/security/guards.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
