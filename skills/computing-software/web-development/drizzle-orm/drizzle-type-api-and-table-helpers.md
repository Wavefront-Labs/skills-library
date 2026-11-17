---
id: computing-software.web-development.drizzle-orm.drizzle-type-api-and-table-helpers
name: drizzle-type-api-and-table-helpers
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, inferselect, inferinsert, getcolumns, gettableconfig]
level: practitioner
status: docs-checked
description: "Infer row types with $inferSelect and $inferInsert, and use getColumns, getTableConfig, is() and pgTableCreator for utilities and shared databases."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/goodies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: derive types and introspect tables in code.

Types (`InferSelectModel` and `InferInsertModel` are imported from `drizzle-orm`):

```ts
type SelectUser = typeof users.$inferSelect;       // or InferSelectModel<typeof users>
type InsertUser = typeof users.$inferInsert;       // or InferInsertModel<typeof users>
```

`getColumns(table)` (from `drizzle-orm`) returns a typed column map, useful when excluding fields from a selection:

```ts
const { password, role, ...rest } = getColumns(users);
await db.select({ ...rest }).from(users);
```

`getTableConfig(table)` (from `drizzle-orm/pg-core`) inspects PostgreSQL table metadata: `const { columns, indexes, foreignKeys, checks, primaryKeys, name, schema } = getTableConfig(table)`.

Use `is(value, Column)` (both from `drizzle-orm`) instead of `instanceof` to check Drizzle object types; the value is narrowed to `Column`.

Multi-project databases: `pgTableCreator((name) => `project1_${name}`)` customizes table names when several projects share one database (the table `users` becomes `project1_users`); the docs pair it with `tablesFilter: ['project1_*']` in `drizzle.config.ts`.

## Checked

Date: 2026-11-07

Confirmed against `pg/goodies.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 185 lines): Type API, Get Typed Columns, Get Table Information, Compare Object Types and Multi-project schema, including imports and the generated `project1_users` SQL.

Removed: `pg/query-utils.mdx` from sources (it only includes a `$count` snippet, which this skill does not cover; the include file was not opened), the explanation that `tablesFilter` stops kit touching other projects' tables and the advice against hand-written DTO types (neither stated), and the invented Verify step. The other sections of goodies.mdx (logging, `.toSQL()`, raw queries, standalone query builder, mock driver) are not covered by this skill.

Method: documentation only; no commands were run.
