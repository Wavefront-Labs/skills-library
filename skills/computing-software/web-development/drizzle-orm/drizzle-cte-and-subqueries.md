---
id: computing-software.web-development.drizzle-orm.drizzle-cte-and-subqueries
name: drizzle-cte-and-subqueries
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, cte, with-clause, subquery, sql-alias]
level: practitioner
status: docs-checked
description: "Use $with CTEs and .as() subqueries in Drizzle select queries, including data-modifying CTEs and the required alias on sql fields."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/select.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split complex queries with CTEs and subqueries.

CTE: `const sq = db.$with('sq').as(db.select().from(users).where(eq(users.id, 42))); const result = await db.with(sq).select().from(sq);`

`insert`, `update` and `delete` statements with `.returning()` can be the body of a `$with` as well:

```ts
const sq = db.$with('sq').as(db.delete(users).where(eq(users.name, 'John')).returning());
await db.with(sq).select().from(sq);
```

Alias rule: arbitrary SQL fields in a CTE must be aliased to be referenced later.

```ts
const sq = db.$with('sq').as(db.select({ name: sql<string>`upper(${users.name})`.as('name') }).from(users));
await db.with(sq).select({ name: sq.name }).from(sq);
```

Without `.as('name')` the field type becomes `DrizzleTypeError`, and ignoring it gives a runtime error because the field cannot be referenced.

Subqueries use `.as('sq')` and work anywhere a table does: `db.select().from(users).leftJoin(sq, eq(users.id, sq.id))`.

The select page links to the insert, update and delete pages for their own `WITH` clause forms (`#with-insert-clause`, `#with-update-clause`, `#with-delete-clause`).

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (select.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
