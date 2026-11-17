---
id: computing-software.web-development.strapi.document-service-publish
name: document-service-publish
category: computing-software
field: web-development
product: strapi
tags: [strapi, document-service, publish, unpublish, discarddraft, draft-and-publish]
level: practitioner
status: docs-checked
description: "publish, unpublish and discardDraft in the Strapi Document Service, only valid with Draft and Publish enabled."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/document-service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Document Service: publishing

These three methods exist only when Draft & Publish is enabled on the content-type.

```js
await strapi.documents('api::restaurant.restaurant').publish({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klmn',
});
```

```js
await strapi.documents('api::restaurant.restaurant').unpublish({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klmn'
});
```

```js
strapi.documents('api::restaurant.restaurant').discardDraft({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klmn',
});
```

- `publish` publishes the draft version.
- `unpublish` moves the published document back to draft.
- `discardDraft` drops draft data and keeps only the published version.

Reads in the Document Service default to the `draft` status. Without a `locale`, `publish()`, `unpublish()` and `discardDraft()` act only on the default locale version.

## Checked

Checked 2026-11-04 against the Strapi Document Service API page (method table, Draft & Publish availability note, `publish`, `unpublish`, `discardDraft`). Removed the claim that REST defaults to `published`, which the page does not state.

Method: documentation only; no commands were run.
