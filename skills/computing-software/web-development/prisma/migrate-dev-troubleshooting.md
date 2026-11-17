---
id: computing-software.web-development.prisma.migrate-dev-troubleshooting
name: migrate-dev-troubleshooting
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-dev-troubleshooting, prisma, history-conflict, schema-drift-fix, db-pull-introspected-change]
level: practitioner
status: docs-checked
description: "Fix development problems with Prisma Migrate such as history conflicts after switching branches, schema drift from manual edits, and failed migrations, using reset or db pull."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/troubleshooting.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Migrate in development

History conflict: the migrations folder and the `_prisma_migrations` table disagree because an applied migration was modified or is missing. Switching feature branches causes this, since the table holds migrations from `branch-1` that disappear on `branch-2`. `migrate dev` detects it and asks to reset and reapply history.

Schema drift: the database differs from the history, for instance after `db push` or manual changes. Detection needs the shadow database, so it is a development-only check.

- Changes you do not want, or can reproduce in the schema: `npx prisma migrate reset`, replicate them in `schema.prisma`, then `npx prisma migrate dev`.
- Changes you want to keep: `npx prisma db pull` to update the schema from the database, then `npx prisma migrate dev --name introspected_change`. Migrate prompts to reset, replays all migrations plus the new one, and the database and history now include your manual changes.

Failed migrations (syntax error in hand-edited SQL, a `NOT NULL` column on a populated table, interrupted process): the `logs` column of `_prisma_migrations` holds the error. Normal fix is to address the cause and reset.

- SQL syntax error: fix the failing `migration.sql`, then `npx prisma migrate reset`.
- Schema change impossible on existing data: delete that `migration.sql`, adjust the schema (for example give the mandatory field a default), run `npx prisma migrate dev` and accept the reset.
- Interrupted: `npx prisma migrate reset`.

For production versions of these problems see `prisma-migrate-failed-migration-recovery` and `prisma-migrate-hotfix-resolve`.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
