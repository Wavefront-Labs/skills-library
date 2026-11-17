---
id: computing-software.web-development.prisma.migrate-failed-migration-recovery
name: migrate-failed-migration-recovery
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-failed-migration-recovery, prisma, migrate-resolve-rolled-back, failed-migration-logs, partial-migration]
level: advanced
status: docs-checked
description: "Recover from a failed production migration either by marking it rolled back and redeploying, or by finishing the steps by hand and resolving it as applied."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/patching-and-hotfixing.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recovering a failed migration in production

A migration can fail because you edited the SQL and made a syntax error, added a `NOT NULL` column to a table with data, the process stopped, or the database shut down mid-migration. The `_prisma_migrations` table has a `logs` column holding the error. While one is in a failed state, `prisma migrate deploy` cannot proceed.

Option 1, roll back and redeploy:

```
npx prisma migrate resolve --rolled-back "<migration-name>"
```

This registers the migration as rolled back so it can apply again. If it ran partially, either make the SQL idempotent (for example `CREATE TABLE ... IF NOT EXISTS`) or manually revert completed steps (delete created tables). Fix the root cause, copy any changed migration back into source control so development matches production, then run `npx prisma migrate deploy`.

Option 2, finish by hand: run the migration steps on production yourself, matching the migration file exactly and copying any edits back to source control, then:

```
npx prisma migrate resolve --applied "<migration-name>"
```

Example failure from the docs: making `User.name` unique fails with `ERROR 1062 (23000): Duplicate entry 'paul' for key 'User_name_key'` because production has duplicate names, after the other statements already ran. Either roll everything back or fix the data and continue forward (see `prisma-migrate-diff-db-execute-recovery`). For development, the usual fix is to repair the cause and run `migrate reset` instead.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
