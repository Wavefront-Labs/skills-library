---
id: computing-software.web-development.prisma.migrate-diff-db-execute-recovery
name: migrate-diff-db-execute-recovery
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-diff-db-execute-recovery, prisma, migrate-diff-script, db-execute-file, config-datasource-flag]
level: advanced
status: docs-checked
description: "Repair a half-applied migration with migrate diff and db execute, going backward to the migration history or forward to the schema, using a production prisma config."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/patching-and-hotfixing.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fixing failed migrations with migrate diff and db execute

`prisma migrate diff` compares two schema sources and prints a summary or, with `--script`, SQL (redirect to a file or pipe to `db execute --stdin`). `prisma db execute` runs a SQL script without touching the migrations table. In Prisma 7 the `--url` flag was removed from `db execute`; configure the production database URL in a config file instead, for example `prisma.config.prod.ts`, and pass `--config prisma.config.prod.ts`.

Backward (revert everything the failed migration did). First get the local history as it was before the failed migration (git, or delete the failed folder locally), then:

```
npx prisma migrate diff \
  --from-config-datasource \
  --to-migrations ./prisma/migrations \
  --config prisma.config.prod.ts \
  --script > backward.sql
npx prisma db execute --config prisma.config.prod.ts --file backward.sql
npx prisma migrate resolve --rolled-back Unique
```

In Prisma 6 the first command used `--from-url "$DATABASE_URL_PROD"` and `--shadow-database-url`, and `db execute` took `--url`.

Forward (fix the bad data first, then complete the change):

```
npx prisma migrate diff --from-config-datasource --to-schema schema.prisma --config prisma.config.prod.ts --script > forward.sql
npx prisma db execute --config prisma.config.prod.ts --file forward.sql
npx prisma migrate resolve --applied Unique
```

Here `Unique` is the failed migration name from the example. Afterwards history and production agree and `migrate dev` / `migrate deploy` work as normal. If you hit `prepared statement "s0" already exists` you are behind PgBouncer (see `prisma-migrate-limitations`).

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
