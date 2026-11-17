---
id: computing-software.web-development.elysia.elysia-prisma-prismabox-validation-models
name: elysia-prisma-prismabox-validation-models
category: computing-software
field: web-development
product: elysia
tags: [integrations-drizzle-prisma, prisma, prismabox, validation, orm]
level: practitioner
status: docs-checked
description: "Generate Elysia validation models from a Prisma schema with the prismabox generator and use them for request and response validation."
sources:
  - https://elysiajs.com/integrations/prisma.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: derive Elysia (TypeBox) models from `schema.prisma` so validation, OpenAPI and Eden share one source.

1. Install:

```bash
bun add @prisma/client prismabox prisma-adapter-bun-sqlite
bun add -d prisma
```

2. Add a generator block to `prisma/schema.prisma`:

```
generator prismabox {
  provider = "prismabox"
  typeboxImportDependencyName = "elysia"
  typeboxImportVariableName = "t"
  inputModel = true
  output   = "../generated/prismabox"
}
```

The docs' client generator uses `provider = "prisma-client"` with `output = "../generated/prisma"`. In Prisma 7+ the datasource URL is configured in the Prisma TypeScript config file (for the CLI), and with driver adapters you also pass the runtime URL in adapter setup.

3. Generate. Each Prisma model gets its own file, e.g. `generated/prismabox/User.ts`, `generated/prismabox/Post.ts`.

4. Use them:

```ts
import { Elysia, t } from 'elysia'
import { PrismaBunSqlite } from 'prisma-adapter-bun-sqlite'
import { PrismaClient } from '../generated/prisma/client'
import { UserPlain, UserPlainInputCreate } from '../generated/prismabox/User'

const adapter = new PrismaBunSqlite({ url: process.env.DATABASE_URL })
export const prisma = new PrismaClient({ adapter })

new Elysia()
    .put('/', async ({ body }) => prisma.user.create({ data: body }),
        { body: UserPlainInputCreate, response: UserPlain })
    .get('/id/:id', async ({ params: { id }, status }) => {
        const user = await prisma.user.findUnique({ where: { id } })
        if (!user) return status(404, 'User not found')
        return user
    }, { response: { 200: UserPlain, 404: t.String() } })
    .listen(3000)
```

Gotchas:
- `typeboxImportDependencyName = "elysia"` with `typeboxImportVariableName = "t"` points generated files at Elysia's `t`.
- The example sets `inputModel = true` and then imports `UserPlainInputCreate` for the body.
- Exact generate command is not given on the page (run Prisma generate as usual).

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/prisma.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
