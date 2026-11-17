---
id: computing-software.web-development.prisma.migrate-limitations
name: migrate-limitations
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-limitations, prisma, switch-database-provider, p3014-error, pgbouncer-prepared-statement]
level: practitioner
status: docs-checked
description: "Known Migrate limits, including no MongoDB support, switching providers with P3014, the PgBouncer prepared statement error and non-interactive environments."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/limitations-and-known-issues.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/troubleshooting.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prisma Migrate limitations

- MongoDB: Migrate does not support the MongoDB connector. Use `db push`.
- Switching providers: migration SQL is provider specific, so one history cannot serve PostgreSQL in production and SQLite in development. A mismatch with `migration_lock.toml` fails with `P3014` ("The datasource provider ... does not match the one specified in the migration_lock.toml"). To switch: change `provider` in the datasource block, update the `url` in the config datasource, archive or remove `prisma/migrations`, and run `prisma migrate dev` to create a new initial migration. That migration only reflects `schema.prisma`, so redo any custom SQL, and the new database has no data.
- Resets lose data: `migrate reset`, or `migrate dev` finding drift or a conflict, drops and recreates the database. These commands are development only.
- PgBouncer: Migrate against a pooled connection can fail with `Error querying the database: db error: ERROR: prepared statement "s0" already exists`. See the PgBouncer page for the workaround; the issue is tracked upstream.
- Non-interactive environments: Docker, Node scripts or bash shells make `migrate dev` print a warning that it is unsupported. In Docker run the image interactively, for example `docker run -it node`.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
