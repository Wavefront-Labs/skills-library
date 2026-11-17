---
id: computing-software.web-development.prisma.migrate-mental-model
name: migrate-mental-model
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-mental-model, prisma, model-first-migration, migrations-table, db-push-vs-migrate, ci-deploy]
level: intro
status: docs-checked
description: "How Prisma Migrate tracks state across schema, history, migrations table and database, and which command each environment uses (dev, db push, deploy)."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/mental-model.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prisma Migrate mental model

Prisma Migrate follows a model-first pattern: you edit the Prisma schema and it generates SQL. Four pieces of state are tracked:

- the Prisma schema (source of truth for structure)
- the migration history, SQL files under `prisma/migrations`
- the `_prisma_migrations` table recording what was applied
- the actual database schema

Per environment:

- Local development: `prisma migrate dev` generates and applies migrations and updates the table. It uses a shadow database to detect drift. Intended only for a disposable development database. If it finds drift or a history conflict it prompts you to reset. `prisma db push` is the alternative for prototyping; it tracks only the schema and the database and writes no migration files.
- Preview or staging, and production: `prisma migrate deploy`, run from CI such as GitHub Actions. It compares applied migrations with the history, applies pending ones, and updates `_prisma_migrations`.

Use `--create-only` with `migrate dev` to edit SQL before it runs (rename a column without data loss, load a Postgres extension). If drift was caused by manual changes, `prisma migrate diff` can generate SQL that reverts the database to the schema or moves it forward, and `prisma db execute` runs that SQL.

Requirements: one database per environment, consistent configuration across environments, and disposable development databases. If you only ever use `db push` you must keep using it in staging and production, and be aware a column rename looks like a drop and create, which prompts a reset.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
