---
id: computing-software.web-development.drizzle-orm.drizzle-pg-constraints
name: drizzle-pg-constraints
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, constraints, unique, check-constraint, foreign-key]
level: practitioner
status: docs-checked
description: "Declare PostgreSQL constraints in Drizzle: unique with NULLS NOT DISTINCT, check, composite primary and foreign keys, and self-references."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/indexes-constraints.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: express constraints in the table's third argument.

The third argument of `pgTable` is a callback returning an array of table-level constraints and indexes.

- Not null: `.notNull()`. Unique: `.unique()`, `.unique('custom_name')`, composite `unique().on(t.id, t.name)`. PostgreSQL 15+: `.unique('n', { nulls: 'not distinct' })` or `unique().on(t.id).nullsNotDistinct()`.
- Check: `check('age_check1', sql`${table.age} > 21`)`.
- Primary key: `.primaryKey()`; composite `primaryKey({ columns: [t.bookId, t.authorId] })`, optionally `name: 'custom_name'`.
- Foreign key inline: `authorId: integer('author_id').references(() => user.id)`.
- Self reference: TypeScript needs an explicit return type, `references((): AnyPgColumn => user.id)`, or use standalone `foreignKey({ columns: [t.parentId], foreignColumns: [t.id], name: 'custom_fk' })`.
- Multi-column foreign key: `foreignKey({ columns: [t.userFirstName, t.userLastName], foreignColumns: [user.firstName, user.lastName] })`.

A primary key constraint automatically has a unique constraint; a table can have many unique constraints but only one primary key.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (indexes-constraints.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
