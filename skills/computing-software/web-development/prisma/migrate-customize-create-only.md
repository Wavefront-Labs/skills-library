---
id: computing-software.web-development.prisma.migrate-customize-create-only
name: migrate-customize-create-only
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-customize-create-only, prisma, create-only, rename-column-migration, change-one-to-one-direction]
level: practitioner
status: docs-checked
description: "Edit generated migration SQL before it runs with migrate dev --create-only, to rename a column instead of dropping it or to move a 1-1 relation foreign key with data."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/customizing-migrations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customizing a migration with --create-only

Procedure: change the schema, then create a draft without applying it, edit the SQL, apply.

```
npx prisma migrate dev --create-only
# edit the generated migration.sql
npx prisma migrate dev
```

Rename a field: Prisma sees a rename as `DROP COLUMN` plus `ADD COLUMN`, which destroys the data. After renaming `biograpy` to `biography` in the schema and running `npx prisma migrate dev --name rename-migration --create-only`, replace the drop and add with a single statement:

```sql
ALTER TABLE "Profile"
RENAME COLUMN "biograpy" TO "biography"
```

The same technique renames a model: rename the table rather than drop and recreate it.

Change the direction of a 1-1 relation: the default draft drops the old foreign key and column then adds a `NOT NULL` column, and the CLI warns that adding a unique constraint fails if duplicate values exist. The documented fix adds the new column nullable, copies data with `UPDATE "User" SET "profileId" = "Profile".id FROM "Profile" WHERE "User".id = "Profile"."userId"`, then `ALTER COLUMN "profileId" SET NOT NULL`, and only then drops the old column.

Other reasons to use it: a large refactor such as `String[]` to a `Tag[]` model, or SQL Prisma schema cannot express such as triggers. Commit the edited file; do not edit it again after it is applied.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
