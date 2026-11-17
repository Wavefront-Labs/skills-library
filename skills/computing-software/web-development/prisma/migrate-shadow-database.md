---
id: computing-software.web-development.prisma.migrate-shadow-database
name: migrate-shadow-database
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-shadow-database, prisma, shadow-database-url, schema-drift-detection, create-database-privilege]
level: advanced
status: docs-checked
description: "What the migrate dev shadow database does, when it is needed, and how to point it at a dedicated database with datasource.shadowDatabaseUrl in prisma.config.ts."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/shadow-database.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/reference/prisma-config-reference.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The shadow database

A temporary database that `prisma migrate dev` creates and deletes automatically. It is used to detect schema drift and to check whether a generated migration could lose data. `migrate diff` also needs one when diffing with `--from-migrations` or `--to-migrations`. It is not needed in production and is not used by `migrate deploy` or `migrate resolve`.

Drift detection: Migrate makes a fresh shadow database, replays the current history, introspects it, and compares that end state to your development database. A mismatch is reported (for example a changed enum variant listed as `[+] Added variant` and `[-] Removed variant`). If there is no drift it computes the new migration, evaluates data loss, applies it unless `--create-only`, and drops the shadow database. Edited or deleted migration files are caught separately by the `checksum` column in `_prisma_migrations`.

When you cannot create or drop databases (some cloud hosts), create a dedicated database and configure it in `prisma.config.ts`:

```ts
export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: {
    url: env("DATABASE_URL"),
    shadowDatabaseUrl: env("SHADOW_DATABASE_URL"),
  },
});
```

A configured shadow database is reset at the start of `migrate dev` rather than dropped. Never use the same value for `url` and `shadowDatabaseUrl`: it may delete all data in your database.

Failure mode: `permission denied to create database` means the user lacks create-database rights. Fix the privileges, use a manual shadow database, or use `prisma db push` while prototyping (see `prisma-migrate-shadow-database-permissions`).

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
