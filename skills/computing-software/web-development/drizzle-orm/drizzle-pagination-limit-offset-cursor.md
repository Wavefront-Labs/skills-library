---
id: computing-software.web-development.drizzle-orm.drizzle-pagination-limit-offset-cursor
name: drizzle-pagination-limit-offset-cursor
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, pagination, limit, offset, cursor-pagination]
level: practitioner
status: docs-checked
description: "Paginate Drizzle queries with limit/offset (always with orderBy), deferred-join subqueries, or cursor pagination using a gt() condition."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/select.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose and implement a pagination strategy.

Limit and offset: `.limit(10).offset(10)`. The docs example comments that `orderBy` is mandatory:

```ts
await db.select().from(users).orderBy(asc(users.id)).limit(4).offset(4);
```

Relational API form:

```ts
db.query.users.findMany({ orderBy: (users, { asc }) => asc(users.id), limit: pageSize, offset: (page - 1) * pageSize });
```

Subquery variant from the docs: select only ids with order, limit and offset in a subquery `.as('subquery')`, then `db.select().from(users).innerJoin(sq, eq(users.id, sq.id)).orderBy(users.id)`.

Cursor pagination:

```ts
const nextUserPage = async (cursor?: number, pageSize = 3) =>
  db.select().from(users)
    .where(cursor ? gt(users.id, cursor) : undefined)
    .limit(pageSize)
    .orderBy(asc(users.id));
```

Pass the cursor (id) of the last row of the previous page, for example `nextUserPage(3)`.

Order helpers: `asc()` and `desc()` from `drizzle-orm`; multiple fields: `.orderBy(asc(users.name), desc(users.name2))`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (select.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
