---
id: computing-software.web-development.drizzle-orm.drizzle-schemas-and-sequences
name: drizzle-schemas-and-sequences
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, pgschema, pgsequence, multi-schema, postgres-schema]
level: practitioner
status: docs-checked
description: "Put tables and enums in named PostgreSQL schemas with pgSchema, and declare sequences with pgSequence and its options."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/schemas.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/sequences.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: organize objects into schemas and sequences.

```ts
import { pgSchema, serial } from "drizzle-orm/pg-core";
export const mySchema = pgSchema("my_schema");
export const colors = mySchema.enum('colors', ['red', 'green', 'blue']);
export const mySchemaUsers = mySchema.table('users', {
  id: serial('id').primaryKey(),
  color: colors('color').default('red'),
});
```

If you declare an entity within a schema, the query builder prepends the schema name in queries (`select * from "schema"."users"`). The page's SQL output shows `CREATE SCHEMA "my_schema";`, then `CREATE TYPE "my_schema"."colors" AS ENUM (...)` and `CREATE TABLE "my_schema"."users" (...)`.

Sequences in PostgreSQL are special single-row tables created to generate unique identifiers, often used for auto-incrementing primary key values, and a thread-safe way to generate unique sequential values across sessions:

```ts
import { pgSchema, pgSequence } from "drizzle-orm/pg-core";
export const customSequence = pgSequence("name");   // no params
export const withParams = pgSequence("name", {
  startWith: 100, maxValue: 10000, minValue: 100, cycle: true, cache: 10, increment: 2,
});
export const inSchema = pgSchema('custom_schema').sequence("name");
```

## Checked

Date: 2026-11-07

Confirmed against `pg/schemas.mdx` (41 lines) and `pg/sequences.mdx` (26 lines) in the drizzle-orm-docs repo (cloned from main, both read in full): schema-name prepending, `pgSchema(...).enum/table`, the generated SQL, the sequence description, `pgSequence` with and without options, and `schema.sequence(...)`.

Removed: the same-name-tables-collide gotcha (it appears only in a commented-out TODO on the page), the `schemaFilter` advice, the export advice (none of these confirmed on these two pages) and the invented Verify step.

Method: documentation only; no commands were run.
