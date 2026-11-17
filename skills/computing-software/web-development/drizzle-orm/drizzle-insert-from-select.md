---
id: computing-software.web-development.drizzle-orm.drizzle-insert-from-select
name: drizzle-insert-from-select
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, insert-select, query-builder, sql-template, cte]
level: advanced
status: docs-checked
description: "Insert rows produced by a query with Drizzle insert().select(), via a query builder, a callback or an sql template, and use WITH clauses on inserts."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/insert.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: copy rows between tables in one statement.

Drizzle supports `insert ... select` for all dialects with one syntax. Three ways:

1. Pass a query builder:

```ts
await db.insert(employees).select(
  db.select({ id: users.id, name: users.name }).from(users).where(eq(users.role, 'employee'))
).returning({ id: employees.id, name: employees.name });
```

A standalone `new QueryBuilder()` (from the dialect core package) also works: `qb.select(...)`.

2. A callback: `.select(() => db.select(...)...)` or `.select((qb) => qb.select(...)...)`.

3. An `sql` template tag with any custom select query, optionally in a callback; the docs example aliases the selected columns (`"users"."id" as "id"`).

Also useful: `with insert`. Define a CTE and use it inside values:

```ts
const userCount = db.$with('user_count').as(db.select({ value: sql`count(*)`.as('value') }).from(users));
await db.with(userCount).insert(users).values([{ username: 'user1', admin: sql`((select * from ${userCount}) = 0)` }]).returning({ admin: users.admin });
```

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (insert.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
