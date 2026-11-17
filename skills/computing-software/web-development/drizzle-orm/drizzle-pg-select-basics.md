---
id: computing-software.web-development.drizzle-orm.drizzle-pg-select-basics
name: drizzle-pg-select-basics
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, select, partial-select, distinct, sql-operator]
level: intro
status: docs-checked
description: "Build typed SELECT queries in Drizzle: full and partial selects, SQL expressions with sql<T>, conditional fields, distinct and distinct on."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/select.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write the common select shapes.

`db.select().from(users)` returns all columns, typed from the table including nullability (`age: number | null`). Drizzle always lists columns explicitly instead of `select *` to guarantee field order.

Partial select: pass an object.

```ts
await db.select({ id: users.id, lowerName: sql<string>`lower(${users.name})` }).from(users);
```

`sql<string>` only tells TypeScript the expected type; Drizzle performs no runtime cast, so a wrong generic yields a value that does not match its type. For runtime conversion use `.mapWith()`.

Conditional field selection: spread an object or empty object: `...(withName ? { name: users.name } : {})`.

Distinct: `db.selectDistinct().from(users).orderBy(users.id, users.name)`. PostgreSQL also supports `db.selectDistinctOn([users.name], { name: users.name }).from(users).orderBy(users.name)`.

Include or exclude columns: `import { getColumns } from 'drizzle-orm'; const { content, ...rest } = getColumns(posts); db.select({ ...rest }).from(posts)`. In the relational API use `columns: { content: false }`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (select.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
