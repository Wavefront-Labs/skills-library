---
id: computing-software.web-development.drizzle-orm.drizzle-relational-queries-find
name: drizzle-relational-queries-find
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relational-queries, findmany, findfirst, with]
level: practitioner
status: docs-checked
description: "Query nested data with db.query.<table>.findMany and findFirst, include relations with with, and rely on a single generated SQL statement."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fetch nested relational data without hand-written joins.

Prerequisite: the client was created with your relations, `drizzle(url, { relations })` where `relations` comes from `defineRelations` (see `drizzle-define-relations-v2`). Then:

```ts
const users = await db.query.users.findMany();
const user = await db.query.users.findFirst();   // adds limit 1
```

Include relations with `with`, nested as deep as needed; Drizzle infers types for nested `with` queries using the Core Type API:

```ts
const users = await db.query.users.findMany({
  with: { posts: { with: { comments: true } } },
});
```

The docs note that Drizzle outputs a single SQL statement for a relational query.

Callback rule (important): in every clause that accepts a callback (`orderBy`, `where.RAW`, `extras` and subqueries inside `extras`), reference columns through the callback parameter, not the imported table object. The callback exposes the aliased table for the current query scope, which the docs say is required for correct SQL generation in nested or self-referential queries (`sql` from `drizzle-orm`):

```ts
db.query.posts.findMany({ orderBy: (t) => sql`${t.id} asc` });          // correct
db.query.users.findMany({ where: { RAW: (t) => sql`LOWER(${t.name}) LIKE 'john%'` } });
```

Aggregations are not supported in `extras`; the docs point to core queries (the SQL-like select API) for them.

## Checked

Date: 2026-11-07

Confirmed against `pg/rqb.mdx` in the drizzle-orm-docs repo (cloned from main, read in full including code tabs): `drizzle(url, { relations })` setup, findMany/findFirst (`limit 1`), nested `with` and Core Type API typing, the single-statement note, the Important callout (callback rule) and the aggregation warning.

Removed: the claim that a single statement makes it safe or cheaper in serverless contexts (not on the page), the "explicit join control" reason for using the SQL-like builder, and the invented Verify step.

Method: documentation only; no commands were run.
