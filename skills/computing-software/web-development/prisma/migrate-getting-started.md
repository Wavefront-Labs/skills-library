---
id: computing-software.web-development.prisma.migrate-getting-started
name: migrate-getting-started
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-getting-started, prisma, migrate-dev, init-migration, migration-folder-naming]
level: intro
status: docs-checked
description: "Create the first Prisma Migrate migration with migrate dev --name, read the timestamped folder it makes, and add later migrations as the schema changes."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/getting-started.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prisma Migrate first migrations

Add models to `schema.prisma` (the `datasource` block names only the `provider` in v7), then create the first migration:

```
npx prisma migrate dev --name init
```

This writes `migrations/<YYYYMMDDHHMMSS>_init/migration.sql` containing the `CREATE TABLE` and foreign key statements for your database. The folder name is the timestamp plus whatever you pass to `--name`. Your schema and database are now in sync and the migration history exists.

For each later schema change (for example adding a `jobTitle String` field) run `migrate dev` again with a new name, such as `--name added_job_title`. The new folder holds only the delta, here an `ALTER TABLE ... ADD COLUMN`. To edit the SQL before it runs, see `prisma-migrate-customize-create-only`.

Use native type attributes such as `@db.VarChar(100)` when you need a specific database type rather than the default mapping (see `prisma-migrate-native-types`).

Commit the whole `migrations` folder with `schema.prisma`; it is what test and production environments replay through `migrate deploy` (see `prisma-migrate-history-source-control` and `prisma-migrate-deploy-production`).

For an existing database that already holds data, do not run `migrate dev` first. Baseline instead (see `prisma-migrate-baseline-existing-database`).

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
