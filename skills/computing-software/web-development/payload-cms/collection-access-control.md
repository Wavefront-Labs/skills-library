---
id: computing-software.web-development.payload-cms.collection-access-control
name: collection-access-control
category: computing-software
field: web-development
product: payload-cms
tags: [collection-access, read-access, query-constraint, readversions]
level: practitioner
status: docs-checked
description: "Write collection access functions for create, read, update, delete, validate, admin, unlock and readVersions, including query constraints."
sources:
  - https://payloadcms.com/docs/access-control/collections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collection access control

Goal: restrict operations on a Collection.

```ts
export const Posts: CollectionConfig = {
  slug: 'posts',
  access: {
    create: ({ req: { user } }) => Boolean(user),
    read: ({ req: { user } }) =>
      user ? true : { _status: { equals: 'published' } },
    update: ({ req: { user } }) => user?.role === 'admin',
    delete: ({ req: { user } }) => user?.role === 'admin',
  },
  fields: [],
}
```

Functions available:

- `create`, `read` (used by `find` and `findByID`), `update`, `delete`. `create` and `admin` return booleans only.
- `validate` - optionally overrides `update` for on-demand validation.
- Auth-enabled collections only: `admin` (who may enter the Admin Panel) and `unlock`.
- Version-enabled collections only: `readVersions` (also restricts the Admin version views).

`read`, `update` and `delete` may return a boolean or a query constraint (a `Where` object) that limits which documents match, for example `{ author: { equals: user.id } }`. Field access cannot return query constraints.

Each function receives an object with `req` (including `req.user`) and operation-specific properties such as `id` or `data`.

`readVersions` falls back to `read` when unset; if set explicitly, a Where query it returns applies to the versions collection.

## Checked

2026-11-04. Read access-control/collections and access-control/fields in the payloadcms/payload docs. Confirmed: function list, query constraints on read/update/delete, field access cannot return query constraints. Added: boolean-only create and admin, readVersions fallback. Removed: the unconfirmed verify step.
Method: documentation only; no commands were run.
