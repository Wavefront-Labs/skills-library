---
id: computing-software.web-development.drizzle-orm.drizzle-generated-columns
name: drizzle-generated-columns
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, generated-columns, generatedalwaysas, stored-column, computed]
level: advanced
status: docs-checked
description: "Add stored generated columns with generatedAlwaysAs using an sql tag or a callback, and respect PostgreSQL limits on them."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/generated-columns.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let the database compute a column.

PostgreSQL supports `STORED` generated columns only: values are computed on insert or update and stored, and can be indexed.

```ts
export const test = pgTable("test", {
  name: text("first_name"),
  generatedName: text("gen_name").generatedAlwaysAs(
    (): SQL => sql`'hi, ' || ${test.name} || '!'`
  ),
});
```

Two forms:
- `sql` tag, when you want Drizzle to escape values for you (the example generates `'hello "world"!'`).
- Callback returning `SQL`, when you need to reference columns of the same table.

`.generatedAlwaysAs()` can be called on any column type.

Database limitations quoted from the docs:
- No default value can be specified.
- The expression cannot reference other generated columns or include subqueries.
- Changing the expression requires a schema change.
- Cannot be used directly in primary keys, foreign keys or unique constraints.

Full-text search example on the page: a `customType` with `dataType()` returning `"tsvector"`, made generated with `to_tsvector('english', ${test.content})`, plus `index("idx_content_search").using("gin", t.contentSearch)`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (generated-columns.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
