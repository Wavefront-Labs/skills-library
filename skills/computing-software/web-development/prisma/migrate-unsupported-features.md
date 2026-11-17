---
id: computing-software.web-development.prisma.migrate-unsupported-features
name: migrate-unsupported-features
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-unsupported-features, prisma, stored-procedure-migration, trigger-migration, partial-index-where]
level: practitioner
status: docs-checked
description: "Add triggers, stored procedures and views to a Prisma Migrate history by editing a --create-only migration, and note partial indexes now use a where argument."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/unsupported-database-features.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unsupported database features in migrations

Some features cannot be written in the Prisma schema: stored procedures, triggers and views, among others. To include them, customize a migration before applying it. Not for MongoDB.

```
npx prisma migrate dev --create-only
```

Open the generated `migration.sql` and add the SQL, for example a trigger function:

```sql
CREATE OR REPLACE FUNCTION notify_on_insert()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pg_notify('new_record', NEW.id::text);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

Then apply with `npx prisma migrate dev` and commit the modified migration.

Partial indexes no longer need this: the schema supports a `where` argument on `@@index`, `@@unique` and `@unique`. Unsupported field types and native database functions can also be expressed in the schema (see `prisma-migrate-native-functions-extensions`).

The native types page lists three routes for unsupported items: handle unsupported field types (such as `circle`), handle unsupported database features such as stored procedures, and use native database functions. Prisma Migrate cannot create features that lack a Prisma Schema Language equivalent on its own.

Remember squashing drops hand-written SQL, so re-add it afterwards (see `prisma-migrate-squash-migrations`), and `migrate diff` cannot invert it for down migrations.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
