---
id: computing-software.web-development.prisma.migrate-down-migrations
name: migrate-down-migrations
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-down-migrations, prisma, down-sql, to-migrations, migrate-rollback]
level: advanced
status: docs-checked
description: "Generate a down.sql with migrate diff before the up migration, store it beside the migration, and run it with db execute and migrate resolve --rolled-back after a failure."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/generating-down-migrations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Generating down migrations

Prisma Migrate has no automatic rollback; you generate the reverse SQL yourself. SQL databases only, not MongoDB. Create the down file first, then the up migration.

1. Edit the schema for the change (the docs add a `Profile` model).
2. Diff from the edited schema back to the state after the last migration. Preferred, since it is more robust:

```
npx prisma migrate diff \
  --from-schema prisma/schema.prisma \
  --to-migrations prisma/migrations \
  --script > down.sql
```

Alternative, comparing to the live database (no shadow database, but the database must be up to date): `--to-config-datasource` in v7 (`--to-schema-datasource` in Prisma 6).

3. Create the up migration: `npx prisma migrate dev --name add_profile`.
4. Copy `down.sql` into the new `<timestamp>_add_profile` folder.

After a failed up migration in production:

```
npx prisma db execute --file ./down.sql
npx prisma migrate resolve --rolled-back add_profile
```

Limits: `migrate resolve` only works on failed migrations; if the up migration succeeded and you want it undone, restore the previous `schema.prisma` and run `migrate dev` to generate a new migration. Data changes made by scripts are not reverted. `migrate diff` cannot invert hand-added SQL, so with custom SQL create the up migration with `migrate dev --create-only`, add the custom SQL, and write the inverse (for example dropping the view) into `down.sql` yourself.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
