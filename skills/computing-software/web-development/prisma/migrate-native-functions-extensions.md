---
id: computing-software.web-development.prisma.migrate-native-functions-extensions
name: migrate-native-functions-extensions
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-native-functions-extensions, prisma, postgresql-extensions, dbgenerated, gen-random-uuid]
level: advanced
status: docs-checked
description: "Use PostgreSQL native functions like gen_random_uuid() with dbgenerated, and enable pgcrypto through the postgresqlExtensions preview feature or a migration."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/native-database-functions.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native functions and PostgreSQL extensions

Some PostgreSQL functions come from extensions. For example in PostgreSQL 12.13 and earlier `gen_random_uuid()` is part of `pgcrypto`. With Prisma Migrate, activate extensions inside a migration, not outside it, because the shadow database needs the same extensions and Migrate recreates it automatically.

Preferred: declare it in the schema with the `postgresqlExtensions` preview feature:

```prisma
generator client {
  provider        = "prisma-client"
  output          = "./generated"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  extensions = [pgcrypto]
}
```

Then apply with Migrate.

Alternative: use the function as a default and add the extension SQL by hand.

```prisma
model User {
  id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
}
```

If the default uses a cast, wrap the whole expression in parentheses: `@default(dbgenerated("(gen_random_uuid()::TEXT)"))`. Run `npx prisma migrate dev --create-only`, add `CREATE EXTENSION IF NOT EXISTS pgcrypto;` at the top of `migration.sql`, then `npx prisma migrate dev`. Resets and new teammates then get the extension from the history.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
