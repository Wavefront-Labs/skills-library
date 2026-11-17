---
id: computing-software.web-development.prisma.migrate-hotfix-resolve
name: migrate-hotfix-resolve
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-hotfix-resolve, prisma, retroactive-migration, schema-drift-hotfix, migrate-resolve]
level: advanced
status: docs-checked
description: "Reconcile history after a manual production change by recreating it in the schema, generating a migration, and marking it applied with migrate resolve."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/patching-and-hotfixing.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reconciling a production hotfix

A manual change in production (say a quick index) causes schema drift. `prisma migrate resolve` reconciles the history without re-running the hotfix. Not for MongoDB.

1. Reproduce the change in `schema.prisma`, for example an `@@index` on a model.
2. Generate the migration locally and note the full folder name with timestamp:

```
npx prisma migrate dev --name retroactively-add-index
```

3. Do not run `migrate deploy` on production. Mark the migration applied there:

```
npx prisma migrate resolve --applied "<full-migration-folder-name>"
```

This adds it to the migrations table without running the SQL.

4. Repeat the resolve on every other database that received the patch (for example staging).
5. Commit the migration so CI applies it to databases that were not patched. Databases where it was resolved as applied skip it.

The migration name passed to `--applied` is the full folder name with its timestamp, as printed by the CLI when the migration was created.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
