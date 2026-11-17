---
id: computing-software.web-development.prisma.migrate-db-push-prototyping
name: migrate-db-push-prototyping
category: computing-software
field: web-development
product: prisma
tags: [prisma-db-push-prototyping, prisma, db-push, accept-data-loss, prototype-schema]
level: practitioner
status: docs-checked
description: "Prototype a schema with db push, know when it errors or needs --accept-data-loss, and move to migrate dev to start a migration history."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/prototyping-your-schema.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prototyping with db push

`npx prisma db push` uses the Migrate engine to make the database match the Prisma schema. It does not create migration files or the `_prisma_migrations` table, and it does not run generators, so run `npx prisma generate` yourself after schema changes. If the change could lose data it errors; add `--accept-data-loss` to proceed.

Good for: fast local iteration, caring about the end state not the steps, and not needing to control data effects. Not good for: replicating changes to other environments without data loss, fine control (renaming rather than drop and create), keeping a change history, or reversibility. For PlanetScale the docs recommend `db push` over `migrate`; MongoDB also uses `db push`.

Example failure: adding a required `description String` to a `Post` table that already has rows makes `db push` fail unless you give a default. Recover with `npx prisma migrate reset` (all data lost) or add a default.

Combine with Migrate:

- New project: iterate with `db push`, then `npx prisma migrate dev --name initial-state` to start history. The prototyping steps are not preserved, only the final state.
- Existing history: prototype with `db push`, then `migrate dev --name added-tags`. Migrate reports "Drift detected" and asks you to reset because the pushed changes are not in the history. Run `npx prisma migrate reset`, after which it replays history and creates the new migration.

Commit the resulting migration and schema.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
