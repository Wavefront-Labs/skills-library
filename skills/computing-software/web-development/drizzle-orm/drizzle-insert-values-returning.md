---
id: computing-software.web-development.drizzle-orm.drizzle-insert-values-returning
name: drizzle-insert-values-returning
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, insert, returning, inferinsert, bulk-insert]
level: intro
status: docs-checked
description: "Insert one or many rows with db.insert().values(), type rows with $inferInsert, and read rows back with returning() in PostgreSQL."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/insert.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: insert rows with correct types.

```ts
await db.insert(users).values({ name: 'Andrew' });
await db.insert(users).values([{ name: 'Andrew' }, { name: 'Dan' }]);
```

Values are parameterized automatically.

Type your input with the inferred insert type (`typeof users.$inferInsert`):

```ts
type NewUser = typeof users.$inferInsert;
const insertUser = async (user: NewUser) => db.insert(users).values(user);
```

Returning (PostgreSQL):

```ts
await db.insert(users).values({ name: 'Dan' }).returning();
await db.insert(users).values({ name: 'Partial Dan' }).returning({ insertedId: users.id });
```

Related: `drizzle-upsert-on-conflict`, `drizzle-insert-from-select`.

Conflicts and upserts (PostgreSQL):

```ts
await db.insert(users).values({ id: 1, name: 'John' }).onConflictDoNothing({ target: users.id });
await db.insert(users).values({ id: 1, name: 'Dan' })
  .onConflictDoUpdate({ target: users.id, set: { name: 'John' } });
```

`onConflictDoUpdate` also takes `targetWhere` (a where on the conflict target, for partial indexes) and `setWhere` (a where on the update), both as `sql` fragments. For composite keys pass an array target: `target: [users.firstName, users.lastName]`.

Insert from a select: `db.insert(employees).select(db.select({ id: users.id, name: users.name }).from(users).where(eq(users.role, 'employee')))`. The select can be a query builder, a callback returning one, or an `sql` template, and the same syntax works across dialects.

A `with` clause can prefix an insert: build a CTE with `db.$with('user_count').as(...)` and call `db.with(userCount).insert(users)...`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (insert.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
