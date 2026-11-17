---
id: computing-software.web-development.django.drf-api-versioning
name: drf-api-versioning
category: computing-software
field: web-development
product: django
tags: [drf-versioning, api-versioning, django-rest-framework, accept-header-versioning, django]
level: practitioner
status: verified
description: "Versioning Django REST Framework APIs: URL path, namespace and Accept header schemes, request.version in serializers and views, default and allowed versions, and deprecating."
sources:
  - https://www.django-rest-framework.org/api-guide/versioning/
  - https://datatracker.ietf.org/doc/html/rfc8594
  - https://drf-spectacular.readthedocs.io/en/latest/faq.html#how-do-i-use-versioning
  - https://www.rfc-editor.org/rfc/rfc8594
  - https://www.rfc-editor.org/rfc/rfc9745
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DRF API versioning

## 1. Pick a scheme
| Scheme | Request | Setting |
|---|---|---|
| URL path | `/api/v2/orders/` | `URLPathVersioning` |
| Namespace | URL include with `namespace="v2"` | `NamespaceVersioning` |
| Accept header | `Accept: application/json; version=2` | `AcceptHeaderVersioning` |
| Query param | `?version=2` | `QueryParameterVersioning` |
| Hostname | `v2.api.example.com` | `HostNameVersioning` |

URL path is the most visible, cache-friendly and easiest for clients; header versioning keeps URLs stable but is harder to test in a browser and requires `Vary: Accept` for caches.

## 2. Configuration
```python
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
}
# urls.py
urlpatterns = [path("api/<str:version>/", include(router.urls))]
```
Requests for versions not in `ALLOWED_VERSIONS` get a 404 (URL path, query parameter) or 406 (Accept header). Put non-versioned routes such as `api/schema/` before `path("api/<str:version>/", ...)`: otherwise `schema` is captured as the version and the request returns 404 "Invalid version in URL path.".

## 3. Behaviour per version
```python
class OrderViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return OrderSerializerV2 if self.request.version == "v2" else OrderSerializerV1
```
- Keep differences in serializers (field names, nesting) rather than duplicating views.
- `reverse("order-detail", kwargs={...}, request=request)` keeps the version in generated URLs.
- Additive changes (new optional fields, new endpoints) don't need a new version; breaking changes (removing/renaming fields, changing types or semantics) do.

## 4. Documentation
drf-spectacular generates per-version schemas: `SpectacularAPIView.as_view(api_version="v2")` (used by the `/api/schema-v2/` URL in testing). `?version=v2` on the schema URL is only consulted when the request has no version of its own: with `URLPathVersioning` and `DEFAULT_VERSION = "v1"` the default wins and `/api/schema/?version=v2` still returned the v1 paths (drf_spectacular `views.py`: `api_version or request.version or ?version`).

## 5. Deprecation
Announce timelines, add `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) headers on old versions via middleware, log usage per version and API key, and contact remaining clients before removal.

## Verify
- [ ] Unknown versions rejected; each version's schema generated and tested; old version responses carry Sunset headers; usage dashboards per version.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: URL-path versioning with `ALLOWED_VERSIONS = ["v1","v2"]`: `/api/v1/orders/1/` returned the V1 serializer fields (`customer`, `id`, `lines`, `note`), `/api/v2/...` the V2 fields (`id`, `note`); `/api/v3/...` -> 404 `Invalid version in URL path.`; DRF `reverse(..., kwargs={"version": request.version, ...}, request=request)` produced `http://testserver/api/v2/orders/1/`.
- Run: `AcceptHeaderVersioning` with `version=9` -> 406 `Invalid version in "Accept" header.`; `QueryParameterVersioning` `?version=9` -> 404, `?version=2` -> 200 with `request.version == "2"`.
- Run: `/api/schema-v2/` (api_version="v2") listed `/api/v2/orders/`, `/api/schema/?version=v2` listed v1 paths; the `api/<str:version>/` include placed first swallowed `api/schema/` (404).
- Fetched: RFC 8594 (The Sunset HTTP Header Field), RFC 9745 (Deprecation HTTP Response Header Field), rfc-editor.org.
