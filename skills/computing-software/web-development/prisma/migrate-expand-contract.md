---
id: computing-software.web-development.prisma.migrate-expand-contract
name: migrate-expand-contract
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-expand-contract, prisma, zero-downtime-migration, dual-write, copy-data-migration]
level: advanced
status: docs-checked
description: "Rename or reshape a column with no downtime using the expand and contract pattern across Prisma migrations and application deployments."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/customizing-migrations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Expand and contract with Prisma Migrate

Changing a column the application uses can cause downtime between the migration and the deployment of code that uses the new shape. The expand and contract pattern splits it into small steps. The docs example renames `bio` to `biography`:

1. Add `biography` to the Prisma schema and create a migration (the old `bio` stays).
2. Expand: change the application to write to both fields, still read from `bio`, and deploy.
3. Create an empty migration to copy data:

```
npx prisma migrate dev --name copy_biography --create-only
```

with SQL `UPDATE "Profile" SET biography = bio;` inside it.

4. Verify the integrity of `biography` in the database.
5. Update the application to read from `biography`.
6. Update the application to stop writing `bio`.
7. Contract: remove `bio` from the schema and run `npx prisma migrate dev --name remove_bio`.

Each step is a deployable change, so schema change and code deploy need less coordination. The docs say the pattern applies to any change to a populated, in-use column, such as combining two fields into one or turning a 1:n relation into m:n.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
