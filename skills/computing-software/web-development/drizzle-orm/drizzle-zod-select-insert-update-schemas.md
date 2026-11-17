---
id: computing-software.web-development.drizzle-orm.drizzle-zod-select-insert-update-schemas
name: drizzle-zod-select-insert-update-schemas
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, zod, createselectschema, createinsertschema, validation]
level: practitioner
status: docs-checked
description: "Generate Zod schemas from Drizzle tables with createSelectSchema, createInsertSchema and createUpdateSchema from drizzle-orm/zod; views and enums supported."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/zod.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: validate API input and output from the table definition.

Starting from `drizzle-orm@1.0.0-beta.15` the standalone `drizzle-zod` package is deprecated in favor of schema generation inside Drizzle ORM (`drizzle-orm/zod`). You can still use `drizzle-zod`, but all new updates go into Drizzle ORM. Install `zod` only.

```ts
import { createSelectSchema, createInsertSchema, createUpdateSchema } from 'drizzle-orm/zod';
const users = pgTable('users', {
  id: integer().generatedAlwaysAsIdentity().primaryKey(),
  name: text().notNull(),
  age: integer().notNull(),
});
```

- Select schema: shape of queried rows, for validating API responses. A partial select such as `{ id, name }` fails against `createSelectSchema(users)` because `age` is missing; `db.select()` of everything passes.
- Insert schema: shape of rows to insert, for validating requests. `{ name: 'John' }` fails because `age` is not defined; `{ name: 'Jane', age: 30 }` parses and can go to `db.insert(users).values(parsed)`. The generated identity `id` is not part of the required input.
- Update schema: every updatable field optional. A generated column such as `id` cannot be updated, so including it fails. Use with `db.update(users).set(parsed).where(...)`.

Views and enums work too: `createSelectSchema(pgEnum('roles', ['admin','basic']))` parses to `'admin' | 'basic'`, and `createSelectSchema(pgView(...).as(...))` gives the view's row shape.

## Checked

Date: 2026-11-07

Confirmed against `zod.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 531 lines including every code block): the deprecation callout, the `zod` install, `drizzle-orm/zod` imports, the select, insert and update examples with their error and success comments, and the view and enum examples.

Removed: the sentence about the other validation libraries' pages (not part of this page) and the invented Verify step. The data type reference at the end of the page was read but is not summarised here.

Method: documentation only; no commands were run.
