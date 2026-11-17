---
id: computing-software.web-development.drizzle-orm.drizzle-join-types
name: drizzle-join-types
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, joins, left-join, inner-join, lateral-join]
level: practitioner
status: docs-checked
description: "Use Drizzle join APIs (left, right, inner, full, cross, and lateral variants) and read the nullable result shapes they produce."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/joins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right join and understand the inferred result type.

Drizzle has `leftJoin`, `rightJoin`, `innerJoin`, `fullJoin`, `crossJoin`, plus PostgreSQL lateral forms `leftJoinLateral`, `innerJoinLateral`, `crossJoinLateral`.

```ts
const result = await db.select().from(users).leftJoin(pets, eq(users.id, pets.ownerId));
```

The default result is one object per row keyed by table name, with nullability inferred from the join type:
- left join: `pets` is `{...} | null`.
- right join: `users` is nullable.
- inner join: neither side is nullable.
- full join: both sides nullable.
- cross join: no ON condition, `db.select().from(users).crossJoin(pets)`; neither side nullable.

Lateral joins take a subquery (built with `.as('userPets')`) and a condition, commonly `sql`true``:

```ts
const subquery = db.select().from(pets).where(gte(users.age, 16)).as('userPets');
await db.select().from(users).leftJoinLateral(subquery, sql`true`);
```

The result key is the subquery alias (`userPets`). `crossJoinLateral(subquery)` takes no condition.

Many-to-many: join through the link table with two joins, for example `from(usersToChatGroups).leftJoin(users, ...).leftJoin(chatGroups, ...).where(eq(chatGroups.id, 1))`.

See `drizzle-join-partial-select-and-aliases` for flat result shapes.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (joins.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
