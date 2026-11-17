---
id: computing-software.web-development.litestar.litestar-dependency-injection
name: litestar-dependency-injection
category: computing-software
field: web-development
product: litestar
tags: [litestar, dependency-injection, provide, named-dependency, scoping, dependencies, use-cache]
level: practitioner
status: docs-checked
description: "Declare Litestar dependencies with Provide on any layer, mark parameters with NamedDependency, chain dependencies and use dependency kwargs."
sources: [https://docs.litestar.dev/latest/usage/dependency-injection.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar dependency injection

Goal: inject shared values into handlers and into other dependencies.

## Method

Declare a `dependencies` dict (string key to `Provide`) on the app, router, controller or handler:

```python
from litestar.di import NamedDependency, Provide

class MyController(Controller):
    path = "/controller"
    dependencies = {"controller_dependency": Provide(list_fn)}

    @get(path="/handler", dependencies={"local_dependency": Provide(int_fn)})
    def my_route_handler(self, app_dependency: NamedDependency[bool],
                         controller_dependency: NamedDependency[list]) -> None: ...

app = Litestar(route_handlers=[my_router], dependencies={"app_dependency": Provide(bool_fn)})
```

Rules:
1. A dependency is a callable (sync or async function, method, instance with `__call__`, or class), wrapped in `Provide`.
2. It may take kwargs and `self`, not positional args.
3. The receiving parameter is marked `NamedDependency[T]` and its name must match the dict key; `T` validates the injected value.
4. It must be in scope: dependencies are isolated to the layer that declares them (a handler-level one is visible only to that handler; only app-level ones reach every handler).

Dependencies can take the same injectable kwargs as handlers (reserved kwargs, path parameters). Example: `async def retrieve_db_user(user_id: UUID4) -> User` provided under key `user` on a controller, consumed with `user: NamedDependency[User]` on `@patch(path="/{user_id:uuid}")`.

Dependencies within dependencies: a provided function can declare `NamedDependency[int]` for another key, e.g. `second_dependency(injected_integer: NamedDependency[int])`, with keys `injected_integer` and `injected_bool` in app `dependencies`.

Caching: with `Provide.use_cache=True` the first return value is memoized, with no kwarg comparison or LRU. Even with `use_cache=False` a dependency is called only once per request.

Defaults: `optional_dependency: NamedDependency[int] = 3` works without providing it, and is excluded from the OpenAPI docs.

## Gotchas

- Injected types are needed at runtime, which can clash with `TYPE_CHECKING` linter rules; use the signature namespace.
- A `NamedDependency` parameter with no default and no provider makes the app fail at startup, not at request time.

## Verify

Starting an app with an unprovided, default-less `NamedDependency` parameter fails at startup, as the page states.

## Checked

2026-11-07. Read the full cited page(s) (usage/dependency-injection.html) and the example files they include, and confirmed the claims in this skill against that text. Removed query parameters from the list of injectable sources (the page names path parameters).

Method: documentation only; no commands were run.
