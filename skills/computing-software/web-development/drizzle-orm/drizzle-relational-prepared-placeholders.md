---
id: computing-software.web-development.drizzle-orm.drizzle-relational-prepared-placeholders
name: drizzle-relational-prepared-placeholders
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, prepared-statements, placeholder, relational-queries, performance]
level: advanced
status: docs-checked
description: "Prepare relational queries with sql.placeholder in where, limit and offset, then execute them repeatedly with different values."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reuse a prepared relational query.

Call `.prepare('name')` on a relational query and `execute` with values for each placeholder (`sql` from `drizzle-orm`):

```ts
const prepared = db.query.users.findMany({
  where: { id: { eq: sql.placeholder('id') } },
  with: { posts: { where: { id: 1 } } },
}).prepare('query_name');
const usersWithPosts = await prepared.execute({ id: 1 });
```

Placeholders are allowed in `limit` and `offset` too, including on nested relations:

```ts
const prepared = db.query.users.findMany({
  with: { posts: { limit: sql.placeholder('limit') } },
}).prepare('query_name');
await prepared.execute({ limit: 1 });
```

```ts
const prepared = db.query.users.findMany({
  offset: sql.placeholder('offset'),
  with: { posts: true },
}).prepare('query_name');
await prepared.execute({ offset: 1 });
```

Multiple placeholders can be mixed, including nested ones:

```ts
const prepared = db.query.users.findMany({
  limit: sql.placeholder('uLimit'),
  offset: sql.placeholder('uOffset'),
  where: { OR: [{ id: { eq: sql.placeholder('id') } }, { id: 3 }] },
  with: {
    posts: {
      where: { id: { eq: sql.placeholder('pid') } },
      limit: sql.placeholder('pLimit'),
    },
  },
}).prepare('query_name');
await prepared.execute({ pLimit: 1, uLimit: 3, uOffset: 1, id: 2, pid: 6 });
```

Each placeholder name is a key of the object passed to `execute`. The docs example gives the top level and the nested level different names (`uLimit` versus `pLimit`).

The page says prepared statements are designed to improve query performance and points to the performance guide (`drizzle-prepared-statements-performance`).

## Checked

Date: 2026-11-07

Confirmed against the "Prepared statements" section of `pg/rqb.mdx` in the drizzle-orm-docs repo (cloned from main, read in full including code tabs): placeholders in `where`, `limit`, `offset`, the multiple-placeholder example and its execute arguments, and the performance sentence.

Removed: the claim to use a distinct statement name per prepared query (not on the page), the fragmentary snippets (replaced with the page's full examples) and the invented Verify step.

Method: documentation only; no commands were run.
