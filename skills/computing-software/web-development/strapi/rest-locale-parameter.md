---
id: computing-software.web-development.strapi.rest-locale-parameter
name: rest-locale-parameter
category: computing-software
field: web-development
product: strapi
tags: [strapi, rest-api, locale, i18n, internationalization, localization]
level: practitioner
status: docs-checked
description: "Read and write locale versions of Strapi documents through the REST locale parameter."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/locale.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# REST `locale`

The locale must already be added in the admin panel. `locale` takes a locale code. If omitted it is the default locale (`en` for new projects, changeable), so `GET /api/restaurants` equals `GET /api/restaurants?locale=en`.

| Use case | Request |
|---|---|
| All documents in a locale | `GET /api/restaurants?locale=fr` |
| One locale version of a document | `GET /api/restaurants/abcdefghijklmno456?locale=fr` |
| Create in default locale | `POST /api/restaurants` + body |
| Create in a locale | `POST /api/restaurants?locale=fr` + body |
| Create or update a locale version of an existing document | `PUT /api/restaurants/abcdefghijklmno456?locale=fr` + body |
| Delete a locale version | `DELETE /api/restaurants/abcdefghijklmno456?locale=fr` |

Single types support GET, PUT and DELETE with `?locale=` on `/api/:singularApiId` (for example `GET /api/homepage?locale=fr`).

- `PUT` with a new locale creates that locale version; with an existing one it updates it. When creating a localization for an existing document the body accepts only localized fields.
- The content-type needs the `createLocalization` permission, otherwise the request returns `403`.
- The locale of an existing entry cannot be changed: a `locale` attribute in the body is ignored.
- `DELETE` returns `204` with no body.

See `computing-software.web-development.strapi.i18n-setup` for enabling localization.

## Checked

2026-11-04: checked against the Strapi docs page REST API: locale (api/rest/locale). Confirmed: locale must already exist in the admin panel, default locale behaviour (`en` for new projects), the six collection-type requests, single-type GET/PUT/DELETE. Corrected: single types do not have a POST create operation, so 'same operations' was wrong. Removed: the claim about where localization is switched on, which this page does not state. Added: createLocalization 403, ignored body locale, 204 on delete.

Method: documentation only; no commands were run.
