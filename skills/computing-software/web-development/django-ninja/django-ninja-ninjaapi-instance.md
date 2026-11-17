---
id: computing-software.web-development.django-ninja.django-ninja-ninjaapi-instance
name: django-ninja-ninjaapi-instance
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, ninjaapi-instance, ninjaapi, constructor, multiple-apis, exception-handler, default-router, openapi]
level: practitioner
status: docs-checked
description: "Configure a NinjaAPI instance: constructor options, default auth, renderer, default_router, several APIs in one project, exception handlers and subclass hooks."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/api.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configure the NinjaAPI instance

Goal: set project-wide behaviour on `NinjaAPI`, and run more than one API.

## Constructor options (all keyword-only)

`title` (default `"NinjaAPI"`), `version` (`"1.0.0"`), `description` (`""`), `openapi_url` (`"/openapi.json"`), `docs` (`Swagger()`), `docs_url` (`"/docs"`), `docs_decorator`, `servers`, `urls_namespace` (defaults to `f"api-{version}"`), `auth`, `throttle`, `renderer` (`JSONRenderer()`), `parser` (`Parser()`), `default_router` (`Router()`), `openapi_extra`.

```python
api = NinjaAPI(
    title="Demo API",
    version="2.0.0",
    description="A demo API with a versioned schema",
    servers=[
        {"url": "https://stag.example.com", "description": "Staging"},
        {"url": "https://prod.example.com", "description": "Production"},
    ],
    openapi_extra={"info": {"termsOfService": "https://example.com/terms/"}},
)
```

Title, version and description only affect the OpenAPI schema and docs page, except that `version` feeds the default `urls_namespace`.

## Default auth and per-operation override

```python
from ninja.security import django_auth

api = NinjaAPI(auth=django_auth)

@api.get("/protected")
def protected(request): ...        # inherits django_auth

@api.get("/public", auth=None)     # None explicitly turns it off
def public(request): ...
```
Leaving the argument out inherits; passing `None` disables. `throttle` works the same way.

## default_router

`@api.get(...)` operations are stored on `api.default_router`. Pass your own `Router` subclass to change all of them, e.g. `NinjaAPI(default_router=RouterPaginated())` (from `ninja.pagination`) paginates every operation whose `response` is a collection.

## Several APIs in one project

```python
api_public = NinjaAPI(auth=django_auth, urls_namespace="public_api")
api_private = NinjaAPI(auth=django_auth_superuser, urls_namespace="private_api")

urlpatterns = [
    path("api/", api_public.urls),
    path("internal-api/", api_private.urls),
]
```
Instances sharing the default `version` must set `version` or `urls_namespace`, otherwise `reverse()` cannot tell their operations apart.

## Exception handlers

Each instance ships default handlers for `Exception`, `Http404`, `HttpError` and Ninja's `ValidationError`. Add your own:

```python
@api.exception_handler(ZeroDivisionError)
def on_zero_division(request, exc):
    return api.create_response(request, {"detail": "Cannot divide by zero"}, status=400)
```

## Subclass hooks

Override `get_openapi_operation_id(self, operation)` (OpenAPI `operationId`) and `get_operation_url_name(self, operation, router)` (Django URL name) on a `NinjaAPI` subclass for API-wide naming.

## Gotcha

Routers must be added before `api.urls` is accessed; `add_router()` afterwards raises `ConfigError`.

## Checked

2026-11-07: Confirmed against guide/api.md, guide/index.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
