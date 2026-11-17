---
id: computing-software.web-development.litestar.litestar-dependency-overrides
name: litestar-dependency-overrides
category: computing-software
field: web-development
product: litestar
tags: [litestar, dependency-injection, dependency-override, skip-validation, openapi, named-dependency, layers]
level: practitioner
status: docs-checked
description: "Override Litestar dependencies by key on a lower layer, exclude defaulted dependencies from OpenAPI, and bypass validation with SkipValidation."
sources: [https://docs.litestar.dev/latest/usage/dependency-injection.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar dependency overrides, OpenAPI exclusion and skipping validation

Goal: replace a dependency at a lower layer and control validation and docs for injected values.

## Method

Overriding: dependencies are string-keyed dicts on each layer, so a lower-scoped declaration with the same key replaces the higher one. The same rule applies to dependencies injected into other dependencies.

```python
class MyController(Controller):
    path = "/controller"
    dependencies = {"some_dependency": Provide(dict_fn)}

    @get(path="/handler", dependencies={"some_dependency": Provide(bool_fn)})
    def my_route_handler(self, some_dependency: NamedDependency[bool]) -> None: ...
```

Here the handler's `bool_fn` overrides the controller's `dict_fn`.

OpenAPI exclusion: give the `NamedDependency` parameter a default. If the dependency is not provided for the route the default is used, and Litestar excludes the parameter from the docs:

```python
@get("/")
async def hello_world(optional_dependency: NamedDependency[int] = 3) -> dict[str, Any]:
    return {"hello": optional_dependency}
```

Validation: injected values are validated against the `NamedDependency[T]` type. With a provider returning `"whoops"` (a `str`) and a handler parameter `injected: NamedDependency[int]`, the application raises an internal server error. Bypass it with the `SkipValidation` marker from `litestar.params`:

```python
from litestar.params import SkipValidation

@get("/", dependencies={"injected": provide_str})
async def hello_world(injected: NamedDependency[SkipValidation[int]]) -> dict[str, Any]:
    return {"hello": injected}
```

## Gotchas

- A `NamedDependency` parameter with no default and no provider fails at startup, not at request time.
- The parameter name must match the dependency key in scope.

## Verify

With `SkipValidation[int]` and a provider returning `"whoops"`, the handler runs and returns `{"hello": "whoops"}` instead of an internal server error (the page contrasts the two examples).

## Checked

2026-11-07. Read the full cited page(s) (usage/dependency-injection.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
