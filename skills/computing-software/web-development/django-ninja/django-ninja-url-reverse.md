---
id: computing-software.web-development.django-ninja.django-ninja-url-reverse
name: django-ninja-url-reverse
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, url-reverse, reverse, url-name, urls-namespace, url-name-prefix, django, reserved-names]
level: practitioner
status: docs-checked
description: "Reverse Django Ninja operation URLs with reverse(), name them with url_name, set urls_namespace, and use url_name_prefix when mounting a router twice."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/urls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL names, namespaces and reverse()

Every operation becomes a normal Django URL pattern with a name inside a namespace.

## Default reverse

Name = the view function's `__name__`; namespace = `"api-" + version` (`api-1.0.0` for a fresh `NinjaAPI()`).

```python
from django.urls import reverse

@api.get("/hello")
def hello(request):
    return {"message": "hello"}

hello_url = reverse("api-1.0.0:hello")  # "/api/hello"
```

Use `reverse_lazy` when the URL is needed before URLconfs load (model field defaults, class attributes).

Stacking several method decorators on one function (`@api.get` plus `@api.post`) yields two patterns sharing the same default name; give each its own `url_name` to reverse them independently.

## Explicit name

```python
@api.get("/users", url_name="user_list")
def users(request):
    return []

reverse("api-1.0.0:user_list")  # "/api/users"
```
An explicit `url_name` always wins. `url_name=""` is treated as not passed.

## Namespaces

Set `urls_namespace` when several `NinjaAPI` instances share a version:

```python
api_public = NinjaAPI(urls_namespace="public_api")
api_private = NinjaAPI(urls_namespace="private_api")
# reverse("public_api:public_users"), reverse("private_api:private_users")
```
Names only need to be unique within a namespace.

## API-wide naming

```python
class MyAPI(NinjaAPI):
    def get_operation_url_name(self, operation, router):
        return operation.view_func.__name__ + "_v2"
```
Used only when the operation set no `url_name`; then `reverse("api-1.0.0:hello_v2")` works.

## Mounting one router twice

```python
api = NinjaAPI()
api.add_router("/v1/things/", things_router)
api.add_router("/v2/things/", things_router, url_name_prefix="things_v2")

reverse("api-1.0.0:list_things")             # /v1/things/
reverse("api-1.0.0:things_v2_list_things")   # /v2/things/
```
Omitting `url_name_prefix` on the second mount raises `ConfigError` right at that `add_router()` call. The prefix applies only to auto-generated names; with explicit `url_name` you must choose unique names yourself.

## Gotchas

- Paths: `{name}` is rewritten to Django's `<name>` syntax and double slashes from joining prefix and path are collapsed (`"/events/"` + `"/"` gives `events/`).
- Reserved names: `openapi-json`, `openapi-view`, `api-root`; do not use them as `url_name`.
- Add all operations and call all `add_router()` before `api.urls` is first accessed; afterwards both raise `ConfigError`.

## Checked
Confirmed 2026-11-08 against the Django Ninja URLs and reverse guide (docs/docs/guide/urls.md, read in full): path rewriting, default name and namespace, `reverse_lazy`, `url_name`, `urls_namespace`, `get_operation_url_name`, `url_name_prefix` and the `ConfigError`, reserved names, and freezing of routers. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
