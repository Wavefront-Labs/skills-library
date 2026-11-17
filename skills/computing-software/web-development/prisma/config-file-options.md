---
id: computing-software.web-development.prisma.config-file-options
name: config-file-options
category: computing-software
field: web-development
product: prisma
tags: [prisma-config-file, prisma, defineconfig, prisma-config-ts, migrations-path-seed]
level: practitioner
status: docs-checked
description: "Write prisma.config.ts with defineConfig or satisfies PrismaConfig, know accepted file names and each option with its default, and load .env via dotenv."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/reference/prisma-config-reference.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# prisma.config.ts

The Prisma CLI is configured in `prisma.config.ts` (created by `prisma init`). Two forms:

```ts
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations", seed: "tsx prisma/seed.ts" },
  datasource: { url: env("DATABASE_URL") },
});
```

or `export default { ... } satisfies PrismaConfig` with `import type { PrismaConfig } from "prisma"`.

File names: `prisma.config.*` or `.config/prisma.*` with extensions `js`, `ts`, `mjs`, `cjs`, `mts`, `cts`. The docs recommend `prisma.config.ts` for small projects and `.config/prisma.ts` for larger ones.

Options:
- `schema`: file or folder (searched recursively for `*.prisma`); default `./prisma/schema.prisma` and `./schema.prisma`.
- `migrations.path`: where migrations live; no default.
- `migrations.seed`: the command `npx prisma db seed` runs; seeding happens only through that command.
- `migrations.initShadowDb`: SQL run on the shadow database first (see `prisma-schema-externally-managed-tables`).
- `views.path` and `typedSql.path`: directories of view SQL and TypedSQL files; no default.
- `tables.external` and `enums.external`: string arrays, default `[]`.
- `experimental.externalTables`: boolean, default `false`. Using external tables without it fails with "The `externalTables` configuration requires `experimental.externalTables` to be set to `true`."
- `datasource.url` (required) and `datasource.shadowDatabaseUrl`.

`.env` files are not loaded automatically: install `dotenv` and import `dotenv/config` on top. Bun loads `.env` itself, so that import can be removed; use `bunx --bun prisma init` so Bun's runtime is used. With a multi-file schema folder, the `migrations` directory must sit next to the `.prisma` file that holds the `datasource` block.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
