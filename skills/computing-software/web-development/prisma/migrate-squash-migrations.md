---
id: computing-software.web-development.prisma.migrate-squash-migrations
name: migrate-squash-migrations
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-squash-migrations, prisma, squashed-migrations, 000000000000-squashed, migrate-diff-script]
level: advanced
status: docs-checked
description: "Squash a feature branch's migrations with migrate dev, or collapse a whole production history into one migration with migrate diff and migrate resolve --applied."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/squashing-migrations.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Squashing migrations

Squashing loses any hand-written SQL (views, triggers) in the migration files; re-add it afterwards.

Squash a feature branch before merging. Preconditions: the migrations to squash are not applied to production, everything applied to production is already in your local history, and none of your new migrations contains custom SQL. Reset `./prisma/migrations` to match `main`, then:

```
npx prisma migrate dev --name squashed_migrations
```

This produces one migration from the `main` state to your current `schema.prisma`, which `migrate deploy` can apply. If production history diverged after you branched, merge the production migrations and data model into your history first.

Collapse a long production history. Preconditions: all migrations applied to production, and the data model and history in sync. Then:

1. Delete the contents of `./prisma/migrations`.
2. Create a directory that sorts first, such as `000000000000_squashed_migrations` (any name that sorts before later ones, like `0_squashed`), with an empty `migration.sql`.
3. Generate it:

```
npx prisma migrate diff \
  --from-empty \
  --to-schema ./prisma/schema.prisma \
  --script > ./prisma/migrations/000000000000_squashed_migrations/migration.sql
```

4. Mark it applied on production: `npx prisma migrate resolve --applied 000000000000_squashed_migrations`.

New checkouts get a single migration; production keeps its old applied rows in the migrations table, and the old files remain in version control.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
