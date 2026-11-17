---
id: computing-software.web-development.drizzle-orm.drizzle-pg-indexes
name: drizzle-pg-indexes
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, indexes, uniqueindex, btree, partial-index]
level: practitioner
status: docs-checked
description: "Declare Drizzle indexes with index() and uniqueIndex(): columns with ordering, concurrently, partial where, with-options and using() for methods and operator classes."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/indexes-constraints.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: declare indexes that drizzle-kit can create.

```ts
export const user = pgTable("user", {
  id: serial().primaryKey(), name: text(), email: text(),
}, (table) => [
  index("name_idx").on(table.name),
  uniqueIndex("email_idx").on(table.email),
]);
```

Builder methods on `index()`/`uniqueIndex()`:
- `.on(table.col1.asc(), table.col2.nullsFirst())` for columns with ordering.
- `.onOnly(...)` takes the same arguments as `.on(...)`.
- `.concurrently()`.
- `.where(sql`...`)` takes a sql expression.
- `.with({ fillfactor: '70' })`.
- `.using('btree', table.col1.asc(), sql`lower(${table.col2})`, table.col1.op('text_ops'))` takes an index method followed by columns, expressions and operator classes.

Placement: indexes go in the third argument of `pgTable`, a callback `(table) => [ ... ]` returning an array (the docs put constraints in the same array; see `drizzle-pg-constraints`).

The docs show the SQL produced for the example above:

```sql
CREATE INDEX "name_idx" ON "user" ("name");
CREATE UNIQUE INDEX "email_idx" ON "user" ("email");
```

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (indexes-constraints.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
