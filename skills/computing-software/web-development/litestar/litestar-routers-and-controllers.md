---
id: computing-software.web-development.litestar.litestar-routers-and-controllers
name: litestar-routers-and-controllers
category: computing-software
field: web-development
product: litestar
tags: [litestar, router, controller, path-nesting, routing, crud, layered-architecture]
level: practitioner
status: docs-checked
description: "Organize Litestar endpoints with Router and Controller classes, nest paths, and understand how paths combine across layers."
sources: [https://docs.litestar.dev/latest/usage/routing/overview.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar routers and controllers

Goal: group handlers under sub-paths using `Router` and `Controller`.

## Method

- `Router` is the base class of `Litestar` itself. It registers controllers, handlers and other routers like the app constructor does, with a `path`.

```python
@get("/{order_id:int}")
def order_handler(order_id: FromPath[int]) -> None: ...


order_router = Router(path="/orders", route_handlers=[order_handler])
base_router = Router(path="/base", route_handlers=[order_router])
app = Litestar(route_handlers=[base_router])
```

`order_handler` is served at `/base/orders/{order_id}`.

- `Controller` subclasses organize endpoints under the controller's `path` class variable using Python OOP; put as many handler methods on it as you like as long as each path+HTTP method pair is unique.

```python
class UserOrderController(Controller):
    path = "/user-order"

    @post()
    async def create_user_order(self, data: JSONBody[UserOrder]) -> UserOrder: ...

    @get(path="/{order_id:uuid}")
    async def retrieve_user_order(self, order_id: FromPath[UUID4]) -> UserOrder: ...

    @patch(path="/{order_id:uuid}", dto=PartialUserOrderDTO)
    async def update_user_order(
        self, order_id: FromPath[UUID4], data: JSONBody[DTOData[PartialUserOrderDTO]]
    ) -> UserOrder: ...

    @delete(path="/{order_id:uuid}")
    async def delete_user_order(self, order_id: FromPath[UUID4]) -> None: ...
```

- The controller path is prefixed to each handler path: `create_user_order` is at `/user-order/`, `retrieve_user_order` at `/user-order/{order_id:uuid}`.
- Without a `path` class variable a controller defaults to the root path `"/"`.
- Register the class itself (not an instance) so each router makes its own instance: `Router(path="/internal", route_handlers=[MyController])`, plus `/partner` and `/consumer`, gives `/internal/controller`, `/partner/controller`, `/consumer/controller`.

## Gotchas

- A router can be registered only once; nest routers as needed, but re-registering one raises an exception.
- The controller `path` is prepended to each handler path; without a `path` on the controller it defaults to `/`.

## Verify

For the router example, a request to `/base/orders/5` reaches `order_handler` with `order_id=5`.

## Checked

2026-11-07. Read the full cited page(s) (usage/routing/overview.html) and the example files they include, and confirmed the claims in this skill against that text. Replaced an unsupported layered guards/dependencies/middleware gotcha with the controller path rules from the page.

Method: documentation only; no commands were run.
