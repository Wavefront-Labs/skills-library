---
id: computing-software.web-development.prisma.client-generated-imports
name: client-generated-imports
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-generated-imports, prisma, browser-ts-enums, models-ts-suffix, commoninputtypes]
level: practitioner
status: docs-checked
description: "Import from the generated client files correctly, client.ts for servers, browser.ts for frontends, enums.ts and models.ts with their Model-suffixed types, never internal."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/generators.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Importing from the generated output

The output folder holds `client.ts`, `browser.ts`, `enums.ts`, `models.ts`, `commonInputTypes.ts`, a `models/` folder with one file per model, and `internal/`.

- `client.ts`: server code. `PrismaClient`, model and utility types, most compatible with `prisma-client-js`; depends on server-only packages, so not for browsers. `import { Prisma, type Post, PrismaClient } from "./generated/prisma/client"`.
- `browser.ts`: frontend-safe, no real `PrismaClient`, includes model and enum types and values, and utilities such as `Prisma.JsonNull` and `Prisma.Decimal`.
- `enums.ts`: slim, backend or frontend; best for tree shaking and typecheck speed when you only need enums: `import { Role } from "./generated/prisma/enums"`.
- `models.ts`: all model types plus derived types such as `PostWhereInput` and `UserUpdateInput`. Plain model types are named `<Model>Model` here (`UserModel`, `PostModel`) to avoid clashing with internal names, whereas `client.ts` and `browser.ts` call it `Post`.
- `models/<Model>.ts`: the same, for a single model.
- `commonInputTypes.ts`: shared helpers like `IntFilter`, rarely needed.
- `internal/*`: do not import. Not stable API; use the `Prisma` namespace from `client.ts` or `browser.ts`.

Splitting into files allows finer imports, which can improve compile and typecheck performance.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/overview/generators pages, orm/v7): generated file layout, client.ts, browser.ts, enums.ts, models.ts and models/<Model>.ts with the Model suffix, commonInputTypes.ts, internal/* warning. The enum import example uses a placeholder enum name.

Method: documentation only; no commands were run.
