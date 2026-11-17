---
id: computing-software.web-development.payload-cms.relationship-field
name: relationship-field
category: computing-software
field: web-development
product: payload-cms
tags: [relationship, relationto, polymorphic, filteroptions]
level: practitioner
status: docs-checked
description: "Define relationship fields with relationTo (one or many collections), hasMany, filterOptions and maxDepth."
sources:
  - https://payloadcms.com/docs/fields/relationship
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Relationship field

Goal: link documents together.

```ts
{ name: 'author', type: 'relationship', relationTo: 'users', required: true },
{ name: 'categories', type: 'relationship', relationTo: 'categories', hasMany: true, minRows: 1 },
{ name: 'placedBy', type: 'relationship', relationTo: ['users', 'organizations'] },
```

Options: `relationTo` (required, one slug or an array for polymorphic), `filterOptions`, `hasMany`, `minRows`, `maxRows`, `maxDepth`, `unique`, `index`, `localized`, plus admin `isSortable`, `allowCreate`, `allowEdit`, `sortOptions`, `appearance`.

Filter selectable options (also validated on the server):

```ts
filterOptions: ({ relationTo, siblingData, user }) =>
  relationTo === 'products' ? { owner: { equals: user?.id } } : true,
```

Polymorphic values come back as `{ relationTo, value }`.

How much of the related document is returned depends on the `depth` of the query (default 1); `maxDepth` caps it for this field regardless of the remaining depth.

Verify: `GET /api/posts?depth=1` returns the author object instead of only its ID.

## Checked

2026-11-04. Read fields/relationship. Confirmed: the config options (relationTo required with one or many slugs, filterOptions, hasMany, minRows, maxRows, maxDepth, unique, index, localized) and admin options (isSortable, allowCreate, allowEdit, sortOptions, appearance), filterOptions arguments including relationTo, siblingData and user, polymorphic values returned as relationTo and value, and depth controlling population.
Method: documentation only; no commands were run.
