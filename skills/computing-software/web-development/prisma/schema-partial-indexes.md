---
id: computing-software.web-development.prisma.schema-partial-indexes
name: schema-partial-indexes
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-partial-indexes, prisma, partialindexes-preview, index-where-raw, filtered-index]
level: advanced
status: docs-checked
description: "Define partial or filtered indexes with where on @unique, @@unique and @@index using raw() or object literals, with the partialIndexes preview feature and database caveats."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/indexes.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/unsupported-database-features.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Partial indexes with where

Supported on PostgreSQL, SQLite, SQL Server and CockroachDB; not MySQL. The `where` argument goes on `@unique`, `@@unique` and `@@index`, and needs the `partialIndexes` preview feature in the generator:

```prisma
generator client {
  provider        = "prisma-client"
  output          = "./generated"
  previewFeatures = ["partialIndexes"]
}
```

Raw SQL predicate (most flexible):

```prisma
@@unique([email], where: raw("status = 'active'"))
@@index([email], where: raw("\"deletedAt\" IS NULL"))
```

Object literal (validated against field types):

```prisma
@@index([title], where: { published: true })
@@unique([email], where: { active: true, deletedAt: null })
```

Values: `Boolean`; string for `String`, `DateTime` and enum fields; numbers for `Int`, `BigInt`, `Float`, `Decimal`; `null` (becomes `IS NULL`); `{ not: value }` (`IS NOT NULL` or `!= value`). Use `raw()` for `Unsupported` or composite types. It combines with other arguments: `@@unique([email], name: "email_active_unique", map: "idx_email_active", where: raw("status = 'active'"))`.

Database behaviour: PostgreSQL, SQLite and SQL Server have full migration and introspection support. CockroachDB can create them but cannot introspect predicate text, so later changes to the `where` clause are not detected by Migrate (it skips predicate comparison). `db pull` adds `partialIndexes` to `previewFeatures` itself and writes the database's normalised predicate as `raw()`, for example PostgreSQL `raw("(status = 'active'::text)")`, which may differ from what you wrote.

Before this feature, partial indexes needed hand-edited migrations (see `prisma-migrate-unsupported-features`).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/indexes and prisma-migrate/workflows/unsupported-database-features pages, orm/v7): supported databases, partialIndexes preview flag, raw() and object-literal syntax, value types table, combining with name and map, per-database behaviour, CockroachDB introspection limit, db pull output, the note that partial indexes no longer need customised migrations.

Method: documentation only; no commands were run.
