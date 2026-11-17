---
id: computing-software.web-development.django-ninja.django-ninja-docs-viewer
name: django-ninja-docs-viewer
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, docs-viewer, swagger, redoc, openapi, docs-url, docs-decorator, interactive-docs]
level: intro
status: docs-checked
description: "Switch Django Ninja docs between Swagger and Redoc, pass Swagger settings, hide the docs UI, or protect it with a view decorator."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/api.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/whatsnew_v1.md
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/settings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose, hide or protect the interactive docs

Goal: control which docs viewer an API serves and who can reach it.

## Pick the viewer

By default the docs are Swagger UI at `/docs`. The viewer is pluggable through the `docs` argument:

```python
from ninja import NinjaAPI, Redoc, Swagger

api = NinjaAPI(docs=Redoc())
api = NinjaAPI(docs=Swagger())
api = NinjaAPI(docs=Swagger({"persistAuthorization": True}))   # pass Swagger config
```

Custom viewers can be written by inheriting `DocsBase`.

## Hide the UI but keep the schema

```python
api = NinjaAPI(docs_url=None)
```
The OpenAPI schema stays available for clients and codegen tools.

## Protect the docs page

`docs_decorator` applies any view decorator to the docs view:

```python
from django.contrib.admin.views.decorators import staff_member_required

api = NinjaAPI(docs_decorator=staff_member_required)
```

## Disable everything

`openapi_url=None` disables the schema and, since the UI depends on the schema, the docs UI too. (`openapi_url` defaults to `/openapi.json`, `docs_url` to `/docs`; both are relative to where `api.urls` is mounted.)

## Notes

- The old `NINJA_DOCS_VIEW` Django setting was removed; setting it raises an exception at startup. Use `docs=` instead.
- Adding `"ninja"` to `INSTALLED_APPS` lets staticfiles serve the docs assets instead of a CDN.
- Swagger and Redoc are available out of the box; see the OpenAPI guide for deeper options.

## Checked

2026-11-07: Confirmed against the NinjaAPI Instance guide (`docs`, `docs_url`, `docs_decorator`, `openapi_url`), the 1.0 release notes (pluggable `Swagger`/`Redoc`, `DocsBase`) and, newly added as a source after reading it, the Settings guide for the removed `NINJA_DOCS_VIEW`. Nothing removed.

Method: documentation only; no commands were run.
