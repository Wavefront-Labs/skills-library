---
id: computing-software.web-development.drizzle-orm.drizzle-upsert-on-conflict
name: drizzle-upsert-on-conflict
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, upsert, on-conflict, onconflictdoupdate, composite-key]
level: practitioner
status: docs-checked
description: "Handle PostgreSQL conflicts in Drizzle with onConflictDoNothing and onConflictDoUpdate, including targets, composite keys, setWhere and targetWhere."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/insert.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write idempotent inserts.

`onConflictDoNothing` cancels the insert if there is a conflict; the target is optional:

```ts
await db.insert(users).values({ id: 1, name: 'John' }).onConflictDoNothing();
await db.insert(users).values({ id: 1, name: 'John' }).onConflictDoNothing({ target: users.id });
```

`onConflictDoUpdate` updates the row if there is a conflict:

```ts
await db.insert(users).values({ id: 1, name: 'Dan' })
  .onConflictDoUpdate({ target: users.id, set: { name: 'John' } });
```

Composite unique index or primary key: `target: [users.firstName, users.lastName]`.

`on conflict do update` can have a `where` clause in two different places, and Drizzle exposes both:
- `targetWhere`, part of the conflict target (for example for partial indexes).
- `setWhere`, part of the `update` clause.

```ts
.onConflictDoUpdate({ target: employees.employeeId, set: { name: 'John Doe' }, setWhere: sql`name <> 'John Doe'` })
.onConflictDoUpdate({ target: employees.employeeId, targetWhere: sql`name <> 'John Doe'`, set: { name: sql`excluded.name` } })
```

To reuse the attempted value, reference `excluded` in SQL, as in `set: { name: sql`excluded.name` }`.

## Checked

Date: 2026-11-07

Confirmed against `pg/insert.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 232 lines): the "Upserts and conflicts" section, both `where` placements with their SQL, the `setWhere`/`targetWhere` examples, `excluded.name` and the composite target example. The remaining sections (returning, multiple rows, `with insert`, insert into select) were read but are not covered here.

Removed: the claim that omitting the target applies to any conflict (the page only shows it omitted), the claim that setWhere "restricts which rows get updated", the statement that PostgreSQL errors when the target matches no unique index (not on the page), and the invented Verify step.

Method: documentation only; no commands were run.
