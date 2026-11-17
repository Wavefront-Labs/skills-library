---
id: computing-software.web-development.prisma.migrate-native-types
name: migrate-native-types
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-native-types, prisma, db-varchar, native-type-attribute, type-mapping]
level: practitioner
status: docs-checked
description: "Choose the exact database column type with native type attributes like @db.VarChar(200) and see how Prisma Migrate renders them into migration SQL."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/native-database-types.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Native database types in migrations

Every feature you can define in the Prisma schema is supported by Prisma Migrate, and each Prisma type has a default database type (for PostgreSQL `String` maps to `text`). A native type attribute selects a specific type:

```prisma
model User {
  id   Int    @id @default(autoincrement())
  name String @db.VarChar(200)
}
```

The generated SQL then uses it, for example `"name" VARCHAR(200) NOT NULL` and a `"title" VARCHAR(150) NOT NULL` for another field. Some Prisma types map to only one native type. Comments and the Prisma-level functions `uuid()` and `cuid()` do not map to database features.

For the full list of mappings see the Prisma schema reference (organised by Prisma type) and the per-database pages for PostgreSQL, MySQL, SQL Server and SQLite (organised by provider). The database features matrix lists which database features map to which schema constructs.

For things with no schema equivalent (stored procedures, triggers, unsupported field types, native functions), use a customized migration instead (see `prisma-migrate-unsupported-features`).

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
