---
id: computing-software.web-development.django-ninja.django-ninja-openapi-docs-config
name: django-ninja-openapi-docs-config
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, openapi-docs, swagger, redoc, docs-url, export-openapi-schema]
level: practitioner
status: docs-checked
description: "Configure Django Ninja OpenAPI docs: Swagger or Redoc, local static assets, hiding or protecting docs, openapi_extra, custom viewer and favicon, schema export."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/openapi.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: customise, secure and export the generated OpenAPI schema and docs UI.

## Defaults
`/openapi.json` (`openapi_url`) and `/docs` (`docs_url`) are registered under the API (e.g. `/api/docs`). The UI is Swagger UI.

## Swagger or Redoc
```python
from ninja import NinjaAPI, Redoc, Swagger
api = NinjaAPI(docs=Redoc())
api = NinjaAPI(docs=Swagger(settings={"persistAuthorization": True}))
api = NinjaAPI(docs=Redoc(settings={"disableSearch": True}))
```
`settings` is merged over defaults and forwarded to the JS library. Swagger defaults: `{"layout": "BaseLayout", "deepLinking": True}`; Redoc has none.

## CDN vs local assets
By default assets come from a CDN and `ninja` need not be in `INSTALLED_APPS`. Add `"ninja"` to `INSTALLED_APPS` to serve them via staticfiles (offline, strict CSP, airgapped).

## Hide or disable
```python
NinjaAPI(docs_url=None)      # hide UI, keep schema
NinjaAPI(openapi_url=None)   # disable schema and UI entirely
```
`openapi_url` and `docs_url` must differ, otherwise an `AssertionError` is raised at startup.

## Protect
```python
from django.contrib.admin.views.decorators import staff_member_required
api = NinjaAPI(docs_decorator=staff_member_required)
```
When an auth class has `csrf` True, Swagger renders with the CSRF token and sends `X-CSRFToken` (not Redoc).

## Extend the schema
```python
api = NinjaAPI(title="Demo API", openapi_extra={"info": {"termsOfService": "https://example.com/terms/"}})
```
Per-operation `openapi_extra` also exists (Operations guide).

## Reverse the docs URL
`reverse("api-1.0.0:openapi-view")` gives `/api/docs`; namespace defaults to `f"api-{version}"`, override with `urls_namespace`.

## Custom viewer and favicon
Subclass `ninja.openapi.docs.DocsBase`, implement `render_page(self, request, api, **kwargs)`; use `self.get_openapi_url(api, kwargs)` for the schema URL. For the favicon, put `"ninja"` in `INSTALLED_APPS` and override template `ninja/favicons.html` (a `{% block favicons %}` with a `<link rel="icon" ...>`).

## Export
```bash
python manage.py export_openapi_schema
python manage.py export_openapi_schema --api project.urls.api --output schema.json --indent 2
```
Options: `--api` (dotted path; default resolves the API mounted at `/api/`), `--output`, `--indent`, `--sorted`, `--ensure-ascii`. Needs `"ninja"` in `INSTALLED_APPS`; pass `--api` if mounted elsewhere or several APIs exist.

## Checked

2026-11-07: Confirmed against guide/openapi.md: every claim, parameter name, default, class, method, example and error string that remains was matched to the page text and its code snippets. Nothing removed.

Method: documentation only; no commands were run.
