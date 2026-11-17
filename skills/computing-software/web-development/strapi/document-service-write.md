---
id: computing-software.web-development.strapi.document-service-write
name: document-service-write
category: computing-software
field: web-development
product: strapi
tags: [strapi, document-service, create, update, delete, documentid]
level: practitioner
status: docs-checked
description: "Create, update and delete documents with strapi.documents(uid) using documentId."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/document-service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Document Service: writing

Documents are addressed by `documentId`, a 24-character alphanumeric string that is a unique, persistent identifier for a content entry, independent of its physical records. The numeric `id` was not always stable in Strapi v4 (it could change on duplication or import/export).

```js
await strapi.documents('api::restaurant.restaurant').create({
  data: {
    name: 'Restaurant B'
  }
})
```

```js
await strapi.documents('api::restaurant.restaurant').update({
    documentId: 'a1b2c3d4e5f6g7h8i9j0klmn',
    data: { name: "New restaurant name" }
})
```

```js
await strapi.documents('api::restaurant.restaurant').delete({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klmn',
})
```

- `create` can target a locale; `delete` can remove a document or one locale version.
- Relations accept `connect`, `disconnect`, `set` (see `computing-software.web-development.strapi.relations-connect-disconnect-set`).
- The Document Service does not sanitize; custom controllers must.

## Checked

Checked 2026-11-04 against the Strapi Document Service API page (`documentId` explanation, relations note, unsanitized-data caution, `create`, `update`, `delete`). Removed the advice to wrap multi-step writes in a transaction and the claim that `id` identifies a record version/locale, neither of which the page states.

Method: documentation only; no commands were run.
