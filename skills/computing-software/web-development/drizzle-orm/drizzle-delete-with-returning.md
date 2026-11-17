---
id: computing-software.web-development.drizzle-orm.drizzle-delete-with-returning
name: drizzle-delete-with-returning
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, delete, returning, with-clause, cte]
level: intro
status: docs-checked
description: "Delete rows in Drizzle with filters, get deleted rows back using returning(), and drive deletes from a CTE."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/delete.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: delete rows and know what was removed.

`await db.delete(users)` deletes all rows in the table, so treat a missing `.where()` as dangerous. With conditions:

```ts
await db.delete(users).where(eq(users.name, 'Dan'));
```

Returning (PostgreSQL):

```ts
const deletedUser = await db.delete(users).where(eq(users.name, 'Dan')).returning();
const deletedUserId = await db.delete(users).where(eq(users.name, 'Dan')).returning({ deletedId: users.id });
```

With clause: compute something once and use it in the filter.

```ts
const averageAmount = db.$with('average_amount').as(
  db.select({ value: sql`avg(${orders.amount})`.as('value') }).from(orders)
);
const result = await db.with(averageAmount).delete(orders)
  .where(gt(orders.amount, sql`(select * from ${averageAmount})`))
  .returning({ id: orders.id });
```

Note the alias on the aggregate (`.as('value')`), required for CTE fields.

The full-row `.returning()` result is an array of deleted rows; the partial form is typed `{ deletedId: number | null }[]`. For `WITH` on select, insert and update, see the sibling pages of the docs.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (delete.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
