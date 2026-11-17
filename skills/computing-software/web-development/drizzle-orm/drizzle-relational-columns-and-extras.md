---
id: computing-software.web-development.drizzle-orm.drizzle-relational-columns-and-extras
name: drizzle-relational-columns-and-extras
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relational-queries, columns, extras, subqueries]
level: practitioner
status: docs-checked
description: "Pick or omit columns in relational queries and add computed fields with extras, including $count subqueries."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shape what a relational query returns.

`columns` includes or omits fields, at the query level, so no additional data is transferred from the database. Drizzle still outputs a single SQL statement:

```ts
await db.query.posts.findMany({ columns: { id: true, content: true }, with: { comments: true } });
await db.query.posts.findMany({ columns: { content: false } });
```

Rules:
- When both `true` and `false` entries are present, all `false` entries are ignored (`{ name: true, id: false }` returns only `name`).
- `columns: {}` with `with: { posts: true }` returns only the nested relation.
- Nested relations accept their own `columns`, for example `comments: { columns: { authorId: false } }`.

`extras` adds computed fields; the key becomes a property on each row:

```ts
await db.query.users.findMany({
  extras: { loweredName: (t, { sql }) => sql<string>`lower(${t.name})` },
  with: { groups: true },
});
```

If you specify `.as("<alias>")` on an extras field, Drizzle ignores it. Extras also work on nested relations (`comments: { extras: { commentSize: ... } }`). Inside `extras`, reference columns through the callback parameter, not the imported table.

Subquery counts (`eq` from `drizzle-orm`):

```ts
extras: { totalPostsCount: (t) => db.$count(posts, eq(posts.authorId, t.id)) }
```

The docs warn that aggregations are not supported in `extras`; use core queries (the SQL-like select API) for them.

## Checked

Date: 2026-11-07

Confirmed against `pg/rqb.mdx` in the drizzle-orm-docs repo (cloned from main, read in full including its code tabs): Partial fields select section (query-level partial select, single SQL statement, true/false rule, `columns: {}`, nested columns), Include custom fields (key becomes a field, `.as()` ignored, nested extras, aggregation warning), Include subqueries (`db.$count` in extras with the callback table) and the Important callout about the callback parameter.

Removed: the invented Verify step.

Method: documentation only; no commands were run.
