---
id: computing-software.web-development.drizzle-orm.drizzle-join-partial-select-and-aliases
name: drizzle-join-partial-select-and-aliases
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, joins, nested-select, self-join, alias]
level: practitioner
status: docs-checked
description: "Flatten join results with partial selects, nested select objects that null a whole table, table aliases for self-joins, and manual row aggregation."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/joins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: shape joined results cleanly.

Partial select on joins gives a flat type and infers nullability: `select({ userId: users.id, petId: pets.id }).from(users).leftJoin(pets, ...)` yields `petId: number | null`.

When you use `sql` fields on the nullable side, you must say so yourself: `sql<string | null>`upper(${pets.name})``. Without the generic the type is `unknown`, and `sql<string>` would lie about nulls.

Nested select objects avoid making every column nullable. Drizzle makes the whole nested object nullable instead:

```ts
await db.select({ userId: users.id, pet: { id: pets.id, name: pets.name } })
  .from(users).fullJoin(pets, eq(users.id, pets.ownerId));
// pet: { id: number; name: string } | null
```

Self-joins need an alias:

```ts
import { alias } from "drizzle-orm/pg-core";
const parent = alias(user, "parent");
await db.select().from(user).leftJoin(parent, eq(parent.id, user.parentId));
```

A self-referencing foreign key is declared with `references((): AnyPgColumn => user.id)`.

Drizzle returns name-mapped rows without restructuring, so one-to-many results repeat the parent. Fold them with a `reduce` into `Record<number, { user: User; pets: Pet[] }>`, pushing `pet` only when it is not null. The relational API is covered in `drizzle-relational-queries-find`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (joins.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
