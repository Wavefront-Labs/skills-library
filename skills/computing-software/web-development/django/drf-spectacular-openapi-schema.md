---
id: computing-software.web-development.django.drf-spectacular-openapi-schema
name: drf-spectacular-openapi-schema
category: computing-software
field: web-development
product: django
tags: [django, drf-spectacular, openapi, django-rest-framework, swagger-ui, api-docs, schema-generation, python, web-development]
level: practitioner
status: verified
description: "Generating accurate OpenAPI 3 schemas for DRF with drf-spectacular: setup, extend_schema for custom views, serializers and enums, CI schema checks and client generation."
sources:
  - https://drf-spectacular.readthedocs.io/en/latest/
  - https://drf-spectacular.readthedocs.io/en/latest/customization.html
  - https://www.django-rest-framework.org/topics/documenting-your-api/
  - https://spec.openapis.org/oas/v3.1.0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI schema with drf-spectacular

**Goal:** a correct, versioned OpenAPI 3 schema generated from code, used for docs, client generation and contract checks.

## 1. Setup
```python
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"}
SPECTACULAR_SETTINGS = {
    "TITLE": "Shop API", "VERSION": "1.4.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,          # separate request/response components (read_only/write_only correct)
}
# urls.py (place these before any catch-all such as path("api/<str:version>/", ...))
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema")),
]
```
DRF's built-in schema generation is deprecated in favour of third-party packages like this.

## 2. Generate and check in CI
```bash
python manage.py spectacular --file schema.yml --validate --fail-on-warn
```
Commit `schema.yml`; CI regenerates and diffs it so API changes are reviewed. The command exited 0 on the sample project (a viewset plus an `extend_schema`-annotated `APIView`) and failed with `--fail-on-warn` once plain `APIView`s without serializers were added.

## 3. Annotate what introspection can't see
```python
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample, inline_serializer

class ReportView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter("month", str, description="YYYY-MM", required=True)],
        responses={200: ReportSerializer, 404: OpenApiResponse(description="No data")},
        tags=["reports"],
    )
    def get(self, request): ...
```
- `APIView`/function views without `serializer_class` log `Error [View]: unable to guess serializer` and are left out of the schema (and `--fail-on-warn` fails) - fix them with `extend_schema`.
- `SerializerMethodField`: annotate the method with `@extend_schema_field(OpenApiTypes.INT)` or a return type hint.
- `@extend_schema_view(list=extend_schema(...), create=...)` for viewsets.
- Duplicate enum names: `ENUM_NAME_OVERRIDES` setting.

## 4. Auth in the schema
Authentication classes are mapped to security schemes automatically (session, token, SimpleJWT). Custom auth classes need an `OpenApiAuthenticationExtension`.

## 5. Use the schema
Generate typed clients (for example `npx openapi-typescript schema.yml -o api.d.ts`, which generated types that `tsc --noEmit` accepted), contract-test with Schemathesis (`schemathesis run LOCATION`, where LOCATION is the schema URL or file), and restrict docs in production if the API is private (`SERVE_PERMISSIONS`, default `AllowAny`).

## Verify
- [ ] `spectacular --validate --fail-on-warn` passes in CI.
- [ ] Generated TypeScript client compiles against the frontend.
- [ ] Schemathesis finds no 500s on the documented endpoints.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: `manage.py spectacular --file schema.yml --validate --fail-on-warn` -> exit 0 for a router viewset plus the `ReportView` snippet; with seven plain `APIView`s the output was `Error [Boom]: unable to guess serializer ...` and "Failing as requested due to warnings".
- Found: the snippet's `OpenApiResponse` was never imported (NameError) - import added.
- Run: `/api/schema/` returned 200 `application/vnd.oai.openapi`, `COMPONENT_SPLIT_REQUEST` produced `OrderRequest` components, `/api/docs/` (Swagger) and `/api/redoc/` returned 200, `SERVE_PERMISSIONS` default is AllowAny, `ENUM_NAME_OVERRIDES` default `{}`.
- Run: `openapi-typescript 7.13.0` on the generated schema, then `tsc --noEmit` passed; `schemathesis 4.32.3 run --help` shows `schemathesis run [OPTIONS] LOCATION`.
- Fetched: DRF `docs/api-guide/schemas.md` (built-in OpenAPI generation deprecated in favour of drf-spectacular).
