---
id: computing-software.web-development.drizzle-orm.drizzle-zod-refinements-and-factory
name: drizzle-zod-refinements-and-factory
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, zod, refinements, createschemafactory, coerce]
level: advanced
status: docs-checked
description: "Customize generated Zod schemas: per-field refinements, overwrite fields, createSchemaFactory with an extended Zod instance, and date coercion."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/zod.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tighten generated schemas without rewriting them.

Each create function takes an optional second parameter keyed by column. A callback extends or modifies the generated field schema; providing a Zod schema overwrites it completely:

```ts
import { z } from 'zod/v4';
const userSelectSchema = createSelectSchema(users, {
  name: (schema) => schema.max(20),        // extends
  bio: (schema) => schema.max(1000),       // extends before becoming nullable/optional
  preferences: z.object({ theme: z.string() }), // overwrites, including nullability
});
```

The docs import `z` from `zod/v4`. Because an overwrite replaces nullability too, `preferences` is required in the example's output type while the extended `bio` stays `bio?: string | undefined`.

Factory for advanced cases, `createSchemaFactory` from `drizzle-orm/zod`:

```ts
import { createSchemaFactory } from 'drizzle-orm/zod';
import { z } from '@hono/zod-openapi';        // extended Zod instance
const { createInsertSchema } = createSchemaFactory({ zodInstance: z });
const s = createInsertSchema(users, { name: (schema) => schema.openapi({ example: 'John' }) });
```

Coercion: `createSchemaFactory({ coerce: { date: true } })` makes the date column `createdAt: timestamp().notNull()` use `z.coerce.date()`. Per the docs, that configuration only coerces dates; set `coerce` to `true` to coerce all data types or specify others.

The page ends with a data type reference mapping column types to Zod schemas, for example boolean columns (`pg.boolean()`, `mysql.boolean()`, `sqlite.integer({ mode: 'boolean' })`) to `z.boolean()`; consult it for other types.

## Checked

Date: 2026-11-07

Confirmed against `zod.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 531 lines including the whole data type reference): the Refinements example and its comments, the Factory functions examples (extended Zod instance and type coercion), and the boolean mapping.

Removed: the unsupported remark that coercion is useful for dates from JSON or forms, the "read only the start of that table" caveat (the whole table was read) and the invented Verify step.

Method: documentation only; no commands were run.
