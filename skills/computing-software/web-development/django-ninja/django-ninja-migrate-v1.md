---
id: computing-software.web-development.django-ninja.django-ninja-migrate-v1
name: django-ninja-migrate-v1
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, migrate-v1, whatsnew, pydantic2, annotated, decorate-view, async-auth, csrf]
level: advanced
status: docs-checked
description: "Upgrade a Django Ninja 0.x project to 1.0: Pydantic 2, Meta class, Form[] syntax, async auth, automatic CSRF, decorate_view and breaking changes."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/whatsnew_v1.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving to Django Ninja 1.0

Install with `pip install -U django-ninja`. v1 supports Python 3.7+; the 0.x series gets only security and critical fixes.

## Breaking changes

- Pydantic v1 is no longer supported (Pydantic 2 only); see the Pydantic migration guide if you used raw models. Plain `Schema` users should have an easy move.
- `resolve_xxx(self, ...)` support is dropped in favour of Pydantic's built-in functionality.
- Python 3.6 is no longer supported.

## Resolvers get a context

```python
class Payload(Schema):
    id: int
    name: str
    request_path: str

    @staticmethod
    def resolve_request_path(data, context):
        request = context["request"]
        return request.get_full_path()
```
The `request` is passed in the validation/serialization context; on responses `response_code` is passed too.

## Meta for ModelSchema

`class Config` is deprecated (still works); use `Meta`, like Django ModelForms:

```python
class TxItem(ModelSchema):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "timestamp"]
```

## Shorter parameter syntax (old syntax still works)

```python
def some_form(request, username: Form[str], password: Form[str]): ...
def some_form(request, data: Form[AuthSchema]): ...
def annotated(request, data: Annotated[SomeData, Form()]): ...
```
replacing `username: str = Form(...)` and `data: AuthSchema = Form(...)`.

## Async authenticators

Add `async` to `authenticate`:

```python
class Auth(HttpBearer):
    async def authenticate(self, request, token):
        if token == "secret":
            return token
```

## CSRF

`csrf=True` is no longer required for cookie-based auth; CSRF protection is enabled automatically, so protected and cookie-less authenticators can be mixed: `NinjaAPI(auth=[django_auth, Auth()])`.

## Other changes

- Docs viewers: `NinjaAPI(docs=Redoc())` / `Swagger({...})`.
- `add_router("/app1", "myproject.app1.router")` string paths.
- Built-in Django decorators such as `cache_page` do not work directly under `@api.get` because Ninja wraps non-`HttpResponse` results; use `decorate_view`:

```python
from ninja.decorators import decorate_view

@api.get("/test")
@decorate_view(cache_page(5))
def test_view(request):
    return str(datetime.now())
```
- `paginate_queryset` now takes the `request` object.

## Checked

2026-11-07: Confirmed against the Django Ninja 1.0 release notes: Pydantic 2 only, Python 3.7+, context in resolvers, `Meta` and the deprecated `Config`, `Form[]` syntax, async authenticators, the CSRF change, docs viewers, string `add_router`, `decorate_view` and `paginate_queryset` taking `request`. Corrected: removed the unsupported advice to "use a static method with context" after the `resolve_xxx(self, ...)` note; the page says only that support was dropped in favour of Pydantic built-ins.

Method: documentation only; no commands were run.
