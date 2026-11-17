---
id: computing-software.web-development.strapi.document-service-read
name: document-service-read
category: computing-software
field: web-development
product: strapi
tags: [strapi, document-service, findone, findfirst, findmany, count]
level: practitioner
status: docs-checked
description: "Read documents server-side with strapi.documents(uid): findOne, findFirst, findMany, count, and what they return by default."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/document-service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Document Service: reading

The recommended back-end API, built on the Query Engine. It is a data-access layer unaware of permissions, so sanitize output in custom controllers.

Methods: `findOne()`, `findFirst()`, `findMany()`, `create()`, `update()`, `delete()`, `publish()`, `unpublish()`, `discardDraft()`, `count()`.

Parameters include `documentId`, `locale`, `status` (`published` | `draft`), `fields`, `populate`, filters.

```js
await strapi.documents('api::restaurant.restaurant').findOne({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klmn'
})
```

`findOne` with only a `documentId` returns the draft version in the default locale.

```js
await strapi.documents('api::restaurant.restaurant').findFirst(
  {
    filters: {
      name: {
        $startsWith: "Pizzeria"
      }
    }
  }
)
```

`findMany` takes the same `filters` shape. `count`:

```js
await strapi.documents('api::restaurant.restaurant').count()
strapi.documents('api::restaurant.restaurant').count({ status: 'published' })
```

Relations, components and dynamic zones are not populated unless you pass `populate`.

Option `documents.strictParams` in `config/api` rejects unrecognized root-level keys.

## Checked

Checked 2026-11-04 against the Strapi Document Service API page (overview, unsanitized-data caution, `strictParams`, `findOne`, `findFirst`, `findMany`, `count`). Nothing removed.

Method: documentation only; no commands were run.
