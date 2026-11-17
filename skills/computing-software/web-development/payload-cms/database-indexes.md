---
id: computing-software.web-development.payload-cms.database-indexes
name: database-indexes
category: computing-software
field: web-development
product: payload-cms
tags: [indexes, compound-indexes, unique-index, index-true]
level: practitioner
status: docs-checked
description: "Speed queries with field-level index: true and compound indexes via the collection indexes option, plus unique fields."
sources:
  - https://payloadcms.com/docs/database/indexes
  - https://payloadcms.com/docs/configuration/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database indexes

Goal: index fields used in filters and sorts.

Single field:

```ts
{ name: 'title', type: 'text', index: true }
```

Compound index on a collection:

```ts
export const MyCollection: CollectionConfig = {
  slug: 'my-collection',
  fields: [{ name: 'title', type: 'text' }, { name: 'createdAt', type: 'date' }],
  indexes: [
    { fields: ['title', 'createdAt'], unique: true }, // unique optional
  ],
}
```

Notes:

- `unique: true` on a field creates a database-level unique index; on a field nested in an array or blocks field it is unique across the whole collection. `id`, `createdAt` and `updatedAt` are indexed by default.
- Index fields that users sort or filter on frequently.
- On MongoDB an indexed localized field gets one index per locale.
- The root `indexSortableFields` option (used with Cosmos DB) indexes sortable fields.

## Checked

2026-11-04. Read database/indexes, configuration/overview (indexSortableFields) and database/mongodb in the payloadcms/payload docs. Confirmed: field index, compound indexes option, unique, indexSortableFields for Cosmos DB. Added: default indexes, nested unique warning, per-locale indexes. Removed: the psql and getIndexes verify step.
Method: documentation only; no commands were run.
