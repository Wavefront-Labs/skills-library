---
id: computing-software.web-development.strapi.content-type-schema-json
name: content-type-schema-json
category: computing-software
field: web-development
product: strapi
tags: [strapi, schema-json, content-type, collection-type, single-type, models]
level: practitioner
status: docs-checked
description: "Anatomy of a Strapi schema.json: kind, collectionName, info names, attributes and options, and where the file lives."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/backend-customization/models.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# schema.json

Two model kinds: content-types (collection or single) and components. Content-types are created with the Content-type Builder or `strapi generate`; files live in `./src/api/[api-name]/content-types/[content-type-name]/`. `schema.json` is generated; `lifecycles.js` must be created manually.

A schema has settings, information, attributes and options.

```json
{
  "kind": "collectionType",
  "collectionName": "Restaurants_v1",
}
```

- `kind`: `collectionType` or `singleType` (content-types only).
- `collectionName`: database table name.

```json
  "info": {
    "displayName": "Restaurant",
    "singularName": "restaurant",
    "pluralName": "restaurants",
    "description": ""
  },
```

`singularName` and `pluralName` generate API routes and tables and should be kebab-case. `icon` picks a Strapi design-system icon.

Options include `privateAttributes` (treat attributes as private even if not defined; merged with the global config) and `draftAndPublish`.

In TypeScript projects, generate schema typings with `ts:generate-types`.

## Checked

Checked 2026-11-04 against the Strapi Models page (content-type files, model settings, information, options). Nothing removed.

Method: documentation only; no commands were run.
