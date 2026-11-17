---
id: computing-software.web-development.payload-cms.collection-config
name: collection-config
category: computing-software
field: web-development
product: payload-cms
tags: [collections, collection-config, slug, useastitle]
level: practitioner
status: docs-checked
description: "Define a Collection with slug, fields, access, hooks, admin options and per-collection features such as auth, upload, versions and trash."
sources:
  - https://payloadcms.com/docs/configuration/collections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collection config

Goal: define a Collection (a group of documents sharing one schema).

```ts
import type { CollectionConfig } from 'payload'

export const Posts: CollectionConfig = {
  slug: 'posts',            // unique, URL-friendly
  admin: { useAsTitle: 'title', defaultColumns: ['title', 'createdAt'] },
  fields: [{ name: 'title', type: 'text', required: true }],
}
```

Top-level options in the docs table: `disableBulkDelete`, `disableBulkEdit`, `admin`, `access`, `auth`, `authorship`, `custom`, `disableDuplicate`, `defaultSort`, `dbName`, `endpoints`, `fields`, `graphQL`, `hooks`, `hierarchy`, `orderable`, `labels`, `enableQueryPresets`, `lockDocuments`, `slug`, `timestamps`, `trash`, `typescript`, `upload`, `versions`, `defaultPopulate`, `indexes`, `select`.

Useful `admin` options: `group` (sidebar grouping, `false` hides it), `useAsTitle` (top-level field used as document title, otherwise the ID), `defaultColumns`, `listSearchableFields`, `hidden`, `preview`, `livePreview`, `components`, `baseFilter`, `pagination`.

- `authorship` (createdBy/updatedBy tracking) is on by default; set `false` to disable. It adds database columns, so relational databases need a migration.
- `defaultSort: '-createdAt'` sorts the List View descending.

## Checked

2026-11-04. Read configuration/collections in the payloadcms/payload docs. Confirmed: option table, admin options, authorship default, defaultSort. Fixed: disableBulkDelete and disableBulkEdit are top-level collection options, not admin options; slug is URL-friendly, not kebab-case. Removed: the restart verify step.
Method: documentation only; no commands were run.
