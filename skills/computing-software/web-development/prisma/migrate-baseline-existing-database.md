---
id: computing-software.web-development.prisma.migrate-baseline-existing-database
name: migrate-baseline-existing-database
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-baseline-existing-database, prisma, baselining, migrate-resolve-applied, migrate-diff-from-empty, db-pull]
level: practitioner
status: docs-checked
description: "Add Prisma Migrate to a database that holds data by writing a 0_init migration with migrate diff and marking it applied with migrate resolve --applied."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/getting-started.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/baselining.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Baselining an existing database

Baselining gives a database that predates Prisma Migrate and cannot be reset (such as production) a migration history, by telling Migrate that the initial migration is already applied. Without it, the generated initial migration tries to create tables that exist and fails. It does not apply to MongoDB, which uses `db push`.

Steps from the docs:

1. Bring `schema.prisma` in sync with the database: `npx prisma db pull`.
2. Move or archive any existing `prisma/migrations` folder and create a fresh one.
3. Add a directory prefixed `0_` (for example `0_init`) so it sorts first lexicographically. A timestamp also works.
4. Generate the SQL:

```
npx prisma migrate diff \
  --from-empty \
  --to-schema prisma/schema.prisma \
  --script > prisma/migrations/0_init/migration.sql
```

5. Review the file. If the database has features Prisma schema cannot express (triggers, functions), append that SQL or replace the file with a `pg_dump` or `mysqldump` output. With `pg_dump`, run `SELECT pg_catalog.set_config('search_path', '', false);` or you hit `The underlying table for model '_prisma_migrations' does not exist.` Order tables so foreign keys are created last, otherwise you see `can't create constraint` errors.
6. Mark it applied: `npx prisma migrate resolve --applied 0_init`.

`resolve --applied` inserts the migration into `_prisma_migrations` without running it. Afterwards `migrate deploy` skips the baseline and applies only later migrations, while a new development database still replays all of them. Compare the resulting schema against production before relying on it, then commit the migrations folder and `schema.prisma`.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
