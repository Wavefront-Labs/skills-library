---
id: computing-software.web-development.drizzle-orm.drizzle-column-name-mapping
name: drizzle-column-name-mapping
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, column-names, casing, snake-case, schema]
level: practitioner
status: docs-checked
description: "By default Drizzle uses the TypeScript key as the column name; use explicit names or the snakeCase builder to map camelCase keys to snake_case columns."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/sql-schema-declaration.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/column-types.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control how TypeScript keys map to database column names.

By default Drizzle uses the TypeScript key as the database column name, so `first_name: varchar()` creates a column `first_name` and `firstName: varchar()` creates `"firstName"`. The column type docs state their examples do not use column-name aliases and rely on keys.

You can give a database name explicitly as the first argument, which keeps idiomatic TypeScript keys while the database stays snake_case:

```ts
export const users = pgTable('users', {
  id: integer('id'),
  firstName: varchar('first_name'),
});
```

To avoid many aliases, the schema page documents a casing builder: `snakeCase` or `camelCase` from `drizzle-orm/pg-core` declare tables whose column keys are mapped to the chosen database convention.

```ts
import { snakeCase } from 'drizzle-orm/pg-core';

export const users = snakeCase.table('users', {
  id: serial().primaryKey(),
  fullName: text(),      // full_name in the database
  createdAt: timestamp(), // created_at in the database
});
```

It is available on all entity types: `snakeCase.table`, `.view`, `.materializedView`, `.schema`, and the same four on `camelCase`. The generated query selects `"id", "full_name", "created_at"`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (sql-schema-declaration.mdx, column-types.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
