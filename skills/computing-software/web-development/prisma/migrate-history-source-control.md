---
id: computing-software.web-development.prisma.migrate-history-source-control
name: migrate-history-source-control
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-history-source-control, prisma, migration-lock-toml, migrations-checksum, edited-migration-warning]
level: practitioner
status: docs-checked
description: "Why the whole migrations folder including migration_lock.toml goes in git, and what happens when an applied migration is edited or deleted."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/migration-histories.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migration history and source control

The history is the `prisma/migrations` folder (one subfolder with a `migration.sql` per migration) plus the `_prisma_migrations` table. The folder is the source of truth for the data model's history; the table lets Migrate check whether a migration ran, whether an applied one was deleted, and whether an applied one was changed.

Commit the entire `prisma/migrations` folder, including `prisma/migrations/migration_lock.toml`, which detects an attempt to switch provider. Committing only `schema.prisma` is not enough: custom SQL you add to migrations cannot be represented in the schema, and `prisma migrate deploy` runs only migration files, never the schema.

Do not edit or delete a migration that has been applied. The docs walk through a seemingly harmless change of `VARCHAR(550)` to `VARCHAR(560)` in an applied migration:

- `migrate dev` errors that a migration changed and suggests a reset.
- After `migrate reset`, the replayed history ends at 560 while the schema says `@db.VarChar(550)`, so Migrate generates another migration to change it back.
- From then on `migrate deploy` warns every run that the migration "has been modified since it was applied", even though end states match.

Such inconsistencies can hide bugs that reproduce in only one environment. When Migrate reports a missing or edited applied migration, restore the file or revert the edit rather than resetting.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
