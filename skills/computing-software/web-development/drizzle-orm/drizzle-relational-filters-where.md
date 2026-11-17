---
id: computing-software.web-development.drizzle-orm.drizzle-relational-filters-where
name: drizzle-relational-filters-where
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relational-queries, where, filter-by-relation, raw-filter]
level: practitioner
status: docs-checked
description: "Filter relational queries with the object where syntax: column operators, AND/OR/NOT, RAW SQL, and filtering parent rows by related rows."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/relations-v1-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write filters in db.query.

The `where` option is an object:

```ts
await db.query.users.findMany({ where: { age: 15, name: 'John' } });     // implicit AND
await db.query.users.findMany({
  where: { OR: [{ id: { gt: 10 } }, { name: { like: 'John%' } }] },
});
await db.query.users.findMany({ where: { NOT: { id: { gt: 10 } }, name: { like: 'John%' } } });
```

Per-column operators listed on the page: `eq, ne, gt, gte, lt, lte, in, notIn, like, ilike, notLike, notIlike, isNull, isNotNull, arrayOverlaps, arrayContained, arrayContains`, plus nested `OR`, `AND`, `NOT`. A bare value (`age: 15`) is compared for equality.

Raw SQL via `RAW`, using the table callback parameter (import `sql` from `drizzle-orm`):

```ts
{ RAW: (table) => sql`${table.preferences}->>'theme' = 'dark'` }
```

Filter by relations: you can filter the parent by any related table you include.

```ts
db.query.usersTable.findMany({ where: { id: { gt: 10 }, posts: { content: { like: 'M%' } } } });
```

Existence check: `where: { posts: true }` keeps only users with at least one post. The migration guide adds `where: { posts: false }` for users without posts, and says that from `1.0.0-rc.5` `where: { posts: {} }` skips the relation filter instead of checking existence.

Nested `with` entries take their own `where`, for example comments created before a date: `comments: { where: { createdAt: { lt: new Date() } } }`.

Optional filters: the migration guide says that from `1.0.0-rc.5` an explicit `undefined` in a relational filter throws. Omit the field, or use `EmptyFilter` (`import { EmptyFilter } from 'drizzle-orm/relations'`) when skipping is intended, for example `id: userId ?? EmptyFilter`. This applies to `db.query` filters, not to the SQL query builder.

This object syntax is Relational Queries v2; the v1 callback form is covered by `drizzle-relations-v1-to-v2-migration`.

## Checked

Date: 2026-11-07

Confirmed against `pg/rqb.mdx` (Select filters, Relations Filters, nested `where`, the Important callout; read in full with its code tabs) and `pg/relations-v1-v2.mdx` (read in full: `where` is now object, optional filters and `EmptyFilter`, relation existence checks, v1 versus v2 naming) in the drizzle-orm-docs repo cloned from main. The operator list was matched to the "List of all filter operators" block.

Removed: the invented Verify step (`.toSQL()` inspection is not on either page). Added the rc.5 undefined and `EmptyFilter` behaviour and `posts: false` from the migration guide, which was added to sources.

Method: documentation only; no commands were run.
