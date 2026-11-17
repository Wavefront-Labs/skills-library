---
id: computing-software.web-development.elysia.elysia-drizzle-typebox-validation-models
name: elysia-drizzle-typebox-validation-models
category: computing-software
field: web-development
product: elysia
tags: [integrations-drizzle-prisma, drizzle, typebox, validation, orm]
level: advanced
status: docs-checked
description: "Reuse a Drizzle table as Elysia validation models with drizzle-typebox, pin @sinclair/typebox, and avoid infinite type instantiation."
sources:
  - https://elysiajs.com/integrations/drizzle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define a table once and reuse it for request validation, OpenAPI and Eden types.

1. Install: `bun add drizzle-orm drizzle-typebox`
2. Pin `@sinclair/typebox` to the minimum version used by `elysia` to avoid Symbol conflicts between two copies. Find it with `grep "@sinclair/typebox" node_modules/elysia/package.json` and set an `overrides` entry in package.json (docs sample: `"@sinclair/typebox": "0.32.4"`).
3. Convert and refine:

```ts
import { t } from 'elysia'
import { createInsertSchema } from 'drizzle-typebox'
import { table } from './database/schema'

const _createUser = createInsertSchema(table.user, {
    email: t.String({ format: 'email' })   // refine a column with Elysia's t
})

new Elysia().post('/sign-up', ({ body }) => { /* create user */ }, {
    body: t.Omit(_createUser, ['id', 'salt', 'createdAt'])
})
```

4. Avoid "Type instantiation is possibly infinite": always assign the `createInsertSchema(...)` result to a variable first and reference it inside `t.Omit`/`t.Pick`. Nesting the call directly inside the Elysia schema causes the circular instantiation.

5. Optional helpers: the docs provide copy-as-is `spread(schema, mode)` and `spreads(models, mode)` utilities (in `src/database/utils.ts`) that turn a Drizzle table or TypeBox object into a plain property map for modes `'insert'` or `'select'`. Then pick fields without `t.Pick`:

```ts
const user = spread(table.user, 'insert')
const createUser = t.Object({ id: user.id, username: user.username, password: user.password })
```

Export a singleton `db = { insert: spreads({ user: table.user }, 'insert'), select: spreads({ user: table.user }, 'select') } as const` and import it anywhere. For refined columns pass `createInsertSchema(table.user, {...})` into `spreads`; `spread` skips already-refined schemas.

Gotchas:
- A version mismatch of `@sinclair/typebox` between drizzle-typebox and Elysia causes conflicting Symbols, per the docs.
- `spread` with a table and mode creates the schema itself; with `undefined` mode it only accepts a TypeBox schema and throws `Expect a schema` otherwise.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/drizzle.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
