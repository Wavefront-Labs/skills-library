---
id: computing-software.web-development.drizzle-orm.drizzle-relational-limit-offset-order
name: drizzle-relational-limit-offset-order
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relational-queries, limit, offset, orderby]
level: practitioner
status: docs-checked
description: "Limit, offset and order both top-level and nested rows in Drizzle relational queries, using object or callback orderBy."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rqb.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound and sort nested results.

Top-level and nested `limit`/`offset`:

```ts
await db.query.posts.findMany({
  limit: 5,
  offset: 2,
  with: { comments: { offset: 3, limit: 3 } },
});
```

The docs flag that `offset` can now be used on nested (`with`) tables as well. "Posts 6 to 10 with comments": `with: { comments: true }, limit: 5, offset: 5`.

Ordering with object syntax:

```ts
await db.query.posts.findMany({
  orderBy: { id: 'asc' },
  with: { comments: { orderBy: { id: 'desc' } } },
});
```

Or SQL/callback form (import `sql` from `drizzle-orm`): `orderBy: (t) => sql`${t.id} asc`` and nested `orderBy: (t, { desc }) => desc(t.id)`.

When you use multiple `orderBy` statements on the same table, they are included in the query in the order you added them.

Callback rule: inside `orderBy` functions reference the callback parameter `t`, never the imported table object.

## Checked

Date: 2026-11-07

Confirmed against `pg/rqb.mdx` in the drizzle-orm-docs repo (cloned from main, read in full including its code tabs): top-level and nested limit/offset example, the nested-offset warning, the "6th to 10th post" example, object orderBy, callback orderBy, the multiple-orderBy ordering note, and the callback rule in the Important callout.

Removed: the advice that row order is not deterministic without orderBy (not stated on the page) and the invented Verify step.

Method: documentation only; no commands were run.
