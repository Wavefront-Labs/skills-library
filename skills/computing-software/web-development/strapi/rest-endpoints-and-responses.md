---
id: computing-software.web-development.strapi.rest-endpoints-and-responses
name: rest-endpoints-and-responses
category: computing-software
field: web-development
product: strapi
tags: [strapi, rest-api, endpoints, documentid, flattened-response, content-api]
level: intro
status: docs-checked
description: "Strapi 5 REST endpoints per content-type, the plural/singular API IDs, and the flattened documentId response shape."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST endpoints

Generated per content-type. `:pluralApiId` and `:singularApiId` come from the "API ID" fields in the Content-Type Builder.

Collection types:

| Method | URL |
|---|---|
| `GET` | `/api/:pluralApiId` |
| `POST` | `/api/:pluralApiId` |
| `GET` | `/api/:pluralApiId/:documentId` |
| `PUT` | `/api/:pluralApiId/:documentId` |
| `DELETE` | `/api/:pluralApiId/:documentId` |

Single types: `GET`, `PUT` (update/create) and `DELETE` on `/api/:singularApiId`.

Upload has its own `/api/upload` endpoints. Components have no endpoints.

## Responses (Strapi 5)
- Flattened: attributes sit directly on `data`, not in `data.attributes`.
- Documents are addressed by `documentId`.
- Keys: `data` (object or array; each has `id`, `documentId`, attributes), `meta` (pagination, publication state...), optional `error`.
- Some plugins (Users & Permissions, Upload) may not follow this format.

## Access
All content types are private by default: make them public or authenticate with proper permissions. Responses hold only top-level fields; relations, media, components and dynamic zones need `populate`.

## Checked

Checked 2026-11-04 against the Strapi REST API page (endpoint tables, upload and component notes, response format, access). Nothing removed.

Method: documentation only; no commands were run.
