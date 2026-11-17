---
id: computing-software.web-development.payload-cms.join-field
name: join-field
category: computing-software
field: web-development
product: payload-cms
tags: [join-field, reverse-relationship, bidirectional, joins-query]
level: advanced
status: docs-checked
description: "Show documents that point at this one with a join field (collection and on), without storing a second source of truth."
sources:
  - https://payloadcms.com/docs/fields/join
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Join field

Goal: expose the reverse side of a relationship.

```ts
// categories collection
{ name: 'relatedPosts', type: 'join', collection: 'posts', on: 'category' }

// posts collection
{ name: 'category', type: 'relationship', relationTo: 'categories' }
```

Options: `name`, `collection` (slug or array), `on` (the relationship or upload field on the other collection, dot notation for nested paths), `orderable` (drag-and-drop ordering via fractional indexing), `where` (hide related docs), `maxDepth` (default 1), `defaultLimit`, `defaultSort`, `access`, `hooks`, `admin` (`defaultColumns`, `allowCreate`, `disableRowTypes`).

Advantages: one source of truth (no syncing two arrays) and no huge ID arrays stored on parents.

The join field stores nothing on the parent document: Payload joins related docs in when you query, at depth 1 or above. It is not supported on DocumentDB or Azure Cosmos DB. Control results per call:

- REST: `?joins[relatedPosts][limit]=5&joins[relatedPosts][sort]=-createdAt`.
- Local API: `joins: { relatedPosts: { limit: 5, sort: '-createdAt', where: {}, count: true } }`.

Verify: query a category with `depth=1` and see `relatedPosts.docs`.

## Checked

2026-11-04. Read fields/join (docs/fields/join.mdx). Confirmed: the config option table (collection, on with dot notation, orderable with fractional indexing, where, maxDepth default 1, defaultLimit, defaultSort, access, hooks, admin options defaultColumns, allowCreate, disableRowTypes), the single-source-of-truth rationale, and the joins query shape with limit, sort, where and count. Added: the DocumentDB and Cosmos DB warning from the page.
Method: documentation only; no commands were run.
