---
id: computing-software.web-development.prisma.client-delete-all-data
name: client-delete-all-data
category: computing-software
field: web-development
product: prisma
tags: [prisma-client-delete-all-data, prisma, truncate-all-tables, deletemany-transaction-order, migrate-reset-test-data]
level: practitioner
status: docs-checked
description: "Wipe all data for dev and tests using ordered deleteMany in a transaction, raw TRUNCATE on PostgreSQL or MySQL, or migrate reset, with the trade-offs of each."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-client/queries/crud.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deleting all data from all tables

Three options from the docs:

1. Ordered `deleteMany` in one transaction. Works on every database when you know the schema:

```ts
await prisma.$transaction([
  prisma.profile.deleteMany(),
  prisma.post.deleteMany(),
  prisma.user.deleteMany(),
]);
```

Order matters: run operations that reference others first, `user` last. Pro: simple, deterministic. Con: on relational databases it scales poorly versus a generic TRUNCATE approach (not an issue on MongoDB).

2. Raw `TRUNCATE`. PostgreSQL: query `pg_tables` for schema `public`, skip `_prisma_migrations`, then `$executeRawUnsafe('TRUNCATE TABLE "public"."A", "public"."B" CASCADE;')`. MySQL: in one `$transaction`, run `SET FOREIGN_KEY_CHECKS = 0;`, each `TRUNCATE`, then `SET FOREIGN_KEY_CHECKS = 1;`, again skipping `_prisma_migrations`. Pros: scalable, very fast. Cons: cannot be undone, and reserved SQL words used as table names can break the raw queries.

3. With Migrate, `migrate reset`: drops the database, creates a new one, applies migrations, then seeds (see `prisma-migrate-dev-and-reset` for the seeding caveat).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-client/queries/crud pages, orm/v7): ordered deleteMany transaction with pros and cons, PostgreSQL and MySQL TRUNCATE approaches and cons, migrate reset steps. Removed a filler paragraph.

Method: documentation only; no commands were run.
