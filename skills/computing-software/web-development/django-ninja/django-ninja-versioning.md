---
id: computing-software.web-development.django-ninja.django-ninja-versioning
name: django-ninja-versioning
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, versioning, api-versions, urls-namespace, multiple-apis, routers]
level: practitioner
status: docs-checked
description: "Version a Django Ninja API by running one NinjaAPI per version at its own URL prefix, sharing routers, or versioning sub-trees of routers."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/versioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: serve multiple API versions. Ninja does not version individual operations; use one `NinjaAPI` instance per version.

## One instance per version
```python
api_v1 = NinjaAPI(version="1.0.0", urls_namespace="api-v1")
api_v2 = NinjaAPI(version="2.0.0", urls_namespace="api-v2")
```
```python
# urls.py
urlpatterns = [
    path("api/v1/", api_v1.urls),
    path("api/v2/", api_v2.urls),
]
```
Each gets its own docs and schema (`/api/v1/docs`, `/api/v2/docs`). `version` and `title` only affect the OpenAPI schema/docs, and Ninja never parses `version`, so `"beta"` or `"2024-01"` are fine.

## Sharing routers across versions
The same `Router` can be added to several APIs; each `add_router()` clones operations onto that API. No `url_name_prefix` is needed (that is only for the same router twice on the same API).

```python
api_v1.add_router("/", router)
api_v2.add_router("/", router)
```
To change one endpoint only in v2, mount the shared router only on v1 and register the new behaviour directly on `api_v2`:
```python
api_v1.add_router("/", router)

@api_v2.get("/items")
def list_items_v2(request):
    return {"results": [{"id": 1, "name": "Widget"}], "count": 1}
```
Operations registered on `api_v2` go to its `default_router`, unrelated to `router`.

## Versioning part of an API
Mount versioned router sub-trees under a single `NinjaAPI`:
```python
api.add_router("/v1/", items_v1)
api.add_router("/v2/", items_v2)
```
One schema and docs page cover both; auth, throttling and exception handlers are configured once.

## Tips
- No built-in request-based versioning (path converter, `Accept` header, query param); it is always which API/Router and which URL prefix.
- If two instances share the same `version` (default `"1.0.0"`), set `urls_namespace` explicitly on at least one, or `reverse()` cannot tell them apart. The namespace defaults to `f"api-{version}"`.
- Set `title`/`description` per instance so each docs page identifies its version.
- Decide routers and versions before `api.urls` is first accessed.

## Checked
Confirmed 2026-11-08 against the Django Ninja versioning guide (docs/docs/guide/versioning.md, read in full): one instance per version, URL mounting and docs paths, free-form `version` strings, router sharing and cloning, v2-only endpoints, sub-tree versioning, and the tips. Nothing removed.
Method: docs-only read of cited pages, 2026-11-08
