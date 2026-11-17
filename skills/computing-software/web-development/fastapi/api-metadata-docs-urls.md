---
id: computing-software.web-development.fastapi.api-metadata-docs-urls
name: api-metadata-docs-urls
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, metadata, openapi-tags, openapi-url, docs-url, redoc-url, license-info]
level: practitioner
status: docs-checked
description: "Set FastAPI title, summary, contact and license metadata, describe tags with openapi_tags, and move or disable the OpenAPI, Swagger UI and ReDoc URLs."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/metadata.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API metadata and docs URLs

## App metadata
Pass to `FastAPI(...)`: `title`, `summary` (since OpenAPI 3.1.0, FastAPI 0.99.0), `description` (Markdown allowed), `version` (your app version, not OpenAPI's), `terms_of_service` (a URL), `contact` (dict: `name`, `url`, `email`), `license_info` (dict: `name` required; `identifier` an SPDX expression, since FastAPI 0.99.0, mutually exclusive with `url`).

## Tag metadata
- `openapi_tags` is a list of dicts: `name` (required, same as in `tags`), `description` (Markdown), `externalDocs` (`description`, required `url`).
- You need not describe every tag.
- The list order sets the display order in the docs UI, not alphabetical order.
- Assign tags with `tags=[...]` on path operations and routers.

## URLs
- OpenAPI schema defaults to `/openapi.json`; change with `openapi_url`. `openapi_url=None` disables the schema and the docs UIs that use it.
- Swagger UI at `/docs` (`docs_url`, `None` disables). ReDoc at `/redoc` (`redoc_url`, `None` disables).

## Verify
Open `/docs` and confirm the title, tag descriptions and ordering.

## Checked

Read the full tutorial/metadata.md source page. Confirmed the title/summary/description/version/terms_of_service/contact/license_info fields (identifier since FastAPI 0.99.0, mutually exclusive with url), openapi_tags keys, tag ordering, and the openapi_url, docs_url and redoc_url defaults and None behaviour. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
