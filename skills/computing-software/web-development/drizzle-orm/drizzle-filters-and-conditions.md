---
id: computing-software.web-development.drizzle-orm.drizzle-filters-and-conditions
name: drizzle-filters-and-conditions
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, where, filters, and-or, parameterized-queries]
level: practitioner
status: docs-checked
description: "Filter Drizzle queries with eq, lt, gte, ne, not, and, or; combine conditions dynamically; values are parameterized automatically."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/select.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write safe, composable WHERE clauses.

Import operators from `drizzle-orm`: `eq, ne, lt, gte, not, and, or`. Use them in `.where()`:

```ts
await db.select().from(users).where(and(eq(users.id, 42), eq(users.name, 'Dan')));
await db.select().from(users).where(not(eq(users.id, 42)));
```

All values passed to operators and to the `sql` tag are parameterized: `eq(users.id, 42)` becomes `where "users"."id" = $1` with params `[42]`.
Because the operators are built on the `sql` function you can write your own:

```ts
function equals42(col: PgColumn) { return sql`${col} = 42`; }
await db.select().from(users).where(equals42(users.id));
```

Interpolating columns (`${users.id}`) instead of hardcoding names means renames in the schema flow into queries.

Dynamic filters: `where(term ? ilike(posts.title, term) : undefined)` is the select page's pattern for an optional filter. For a list, build `const filters: SQL[] = []`, push `ilike`, `inArray`, `gt` conditions, then `.where(and(...filters))`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (select.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
