---
id: computing-software.web-development.drizzle-orm.drizzle-schema-files-and-config
name: drizzle-schema-files-and-config
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, schema, drizzle-kit, schema-ts, project-layout]
level: intro
status: docs-checked
description: "Declare Drizzle tables in one or many TypeScript files and point drizzle-kit at them so every exported model reaches the migration diff."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/sql-schema-declaration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a schema layout that drizzle-kit can read completely.

The schema is the source of truth for both queries (drizzle-orm) and migrations (drizzle-kit). Declare tables with the dialect-specific builder, for PostgreSQL `pgTable` from `drizzle-orm/pg-core`. A table should have at least one column, and there is no common table object across dialects: you choose PostgreSQL, MySQL, SQLite and so on.

```ts
import { integer, pgTable, varchar } from "drizzle-orm/pg-core";

export const usersTable = pgTable("users", {
  id: integer().primaryKey().generatedAlwaysAsIdentity(),
  name: varchar().notNull(),
  email: varchar().notNull().unique(),
});
```

The page shows three declaration styles: named imports, a callback `pgTable("users", (t) => ({ id: t.integer() ... }))`, or `import * as p from "drizzle-orm/pg-core"`.

By default Drizzle uses the TypeScript key names as column names; give a name to differ, for example `firstName: varchar('first_name')`.

Layout options (the file name is free, for example `models.ts`):
- One file, for example `src/db/schema.ts`, with `schema: './src/db/schema.ts'` in `drizzle.config.ts`.
- Many files in a folder, `schema: './src/db/schema'`. Drizzle reads the folder, finds all files recursively and gets the tables from there. Group per table or per domain (users, messaging, products).

Rule: export all the models (tables, enums, sequences and so on) from your schema files so Drizzle Kit can import them and use them in the migration diff.

Config skeleton:

```ts
import { defineConfig } from "drizzle-kit";
export default defineConfig({ dialect: 'postgresql', schema: './src/db/schema' });
```

## Checked

Date: 2026-11-07

Confirmed against `pg/sql-schema-declaration.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 393 lines including the example schema): source-of-truth wording, the export callout, the three declaration styles, one-file and multi-file layouts with config paths, recursive discovery, at-least-one-column and no-common-table-object statements, key-name default.

Removed: the claim that anything not exported will not be in generated migrations (the page only says to export so the migration diff can import them) and the invented Verify step. Not summarised: the snakeCase/camelCase builders, schemas and the example project schema at the end of the page.

Method: documentation only; no commands were run.
