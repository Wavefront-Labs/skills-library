---
id: computing-software.web-development.strapi.relations-connect-disconnect-set
name: relations-connect-disconnect-set
category: computing-software
field: web-development
product: strapi
tags: [strapi, relations, connect, disconnect, set, rest-api, document-service]
level: advanced
status: docs-checked
description: "Change Strapi relations in request bodies with connect, disconnect and set, shorthand vs longhand, and the TypeScript TS2353 workaround."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/relations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# connect, disconnect, set

Work in REST, GraphQL and Document Service payloads, for single and multi relations.

| Param | Effect |
|---|---|
| `connect` | partial update; connects entities; combinable with `disconnect`; supports positional arguments for ordering |
| `disconnect` | partial update; combinable with `connect` |
| `set` | full update; overwrites all existing connections; cannot be combined with `connect`/`disconnect` |

`connect` shorthand vs longhand:

```js
connect: ['z0y2x4w6v8u1t3s5r7q9onm', 'j9k8l7m6n5o4p3q2r1s0tuv']
connect: [{ documentId: 'z0y2x4w6v8u1t3s5r7q9onm' }, { documentId: 'j9k8l7m6n5o4p3q2r1s0tuv' }]
```

Longhand is also used to reorder relations: each item takes an optional `position` of `{ before: documentId }`, `{ after: documentId }`, `{ start: true }` or `{ end: true }`. Without `position` the default is `{ end: true }`. Items in the `connect` array are processed sequentially, and the same relation must not be connected twice (validation error).

For one-to-one, many-to-one and one-way relations only the last relation is used, so prefer the short form, for example `data: { category: 'a1b2c3d4e5f6g7h8i9j0klm' }`.

Omitting `connect`, `disconnect` and `set` is equivalent to `set`: `data: { categories: ['id1', 'id2'] }` replaces all existing relations.

When the source has i18n or Draft & Publish off and the target has it on, a longhand item can pick the target version with `locale: 'fr'` or `status: 'draft'`/`'published'`.

With i18n, pass `locale` to set relations for that locale; without it the default locale is assumed:

```js
await strapi.documents('api::restaurant.restaurant').update({
  documentId: 'a1b2c3d4e5f6g7h8i9j0klm',
  locale: 'fr',
  data: {
    category: {
      connect: ['z0y2x4w6v8u1t3s5r7q9onm', 'j9k8l7m6n5o4p3q2r1s0tuv']
    }
  }
})
```

`connect` is not officially supported for media attributes.

## TypeScript TS2353
Typings may reject `connect` although runtime supports it. The page's workaround: `order: { connect: [order.documentId] } as any`.

## Checked

2026-11-04: checked against the Strapi docs page Relations (api/rest/relations). Confirmed: the three parameters and their partial or full update types, shorthand and longhand connect syntax, the locale example and default-locale rule, the media caution, the TS2353 note and workaround. Added from the page: position options and default, sequential processing, duplicate connect error, last-relation-only rule, omitting parameters equals set, locale/status targeting.

Method: documentation only; no commands were run.
