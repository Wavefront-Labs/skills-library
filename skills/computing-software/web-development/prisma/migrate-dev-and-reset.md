---
id: computing-software.web-development.prisma.migrate-dev-and-reset
name: migrate-dev-and-reset
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-dev-and-reset, prisma, migrate-reset, reset-prompt, skip-seed, development-only]
level: practitioner
status: docs-checked
description: "What migrate dev and migrate reset do step by step, when they prompt for a reset, and why neither belongs in production."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/development-and-production.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/prototyping-your-schema.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# migrate dev and migrate reset

`npx prisma migrate dev` is a development command and must never run against production. It:

- replays the existing history in the shadow database to detect drift (edited or deleted migration, or manual database changes)
- applies pending migrations (for example a colleague's) to the shadow database
- generates a new migration if the Prisma schema changed
- applies all unapplied migrations to the development database and updates `_prisma_migrations`
- triggers artifact generation such as Prisma Client

It prompts you to reset when the history has conflicts from modified or missing migrations, or when the database drifted from the end state of the history.

`npx prisma migrate reset` is also development only. It drops the database or schema if it can (for MySQL and MongoDB this means the database, for PostgreSQL and SQL Server the schema, for SQLite the file) or performs a soft reset where deletion is not allowed, recreates it, and applies all migrations. Run `npx prisma db seed` afterwards to repopulate data.

Tip from the docs: if schema changes mean your seed script no longer works, pass `--skip-seed` to `migrate dev`. Seeding in v7 is explicit only (see `prisma-migrate-seeding`).

Typical reset trigger after prototyping: you ran `db push` and hand edits, then `migrate dev --name added-tags` reports "Drift detected" and asks to reset. This causes total data loss in that database.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
