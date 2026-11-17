---
id: computing-software.web-development.payload-cms.database-migrations
name: database-migrations
category: computing-software
field: web-development
product: payload-cms
tags: [migrations, migrate-create, prodmigrations, push-mode]
level: advanced
status: docs-checked
description: "Create, run and roll back migrations with the payload CLI, write up/down functions, and run them at startup with prodMigrations."
sources:
  - https://payloadcms.com/docs/database/migrations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database migrations

Goal: manage schema and data changes safely.

Add a `payload` script to package.json and always run through your package manager:

```json
{ "scripts": { "payload": "cross-env PAYLOAD_CONFIG_PATH=src/payload.config.ts payload" } }
```

Migration files live in `./src/migrations` by default (`migrationDir` changes it) and export `up` and `down`:

```ts
import { MigrateUpArgs, MigrateDownArgs } from '@payloadcms/db-postgres'
export async function up({ payload, req }: MigrateUpArgs): Promise<void> {}
export async function down({ payload, req }: MigrateDownArgs): Promise<void> {}
```

Commands: `migrate`, `migrate:create [name]` (flags `--skip-empty` to skip the empty-migration prompt on Postgres, `--force-accept-warning`), `migrate:status`, `migrate:down` (last batch), `migrate:refresh`, `migrate:reset`, `migrate:fresh` (drops everything and reruns).

When needed: relational databases require migrations outside development (use `push` locally, then `migrate:create` and `migrate` in CI before deploying). MongoDB only needs them to transform existing data.

Run at startup on long-running servers:

```ts
db: postgresAdapter({ pool: { connectionString: process.env.DATABASE_URL }, prodMigrations: migrations })
```

Warning: this can slow serverless cold starts.

`down` is also called if a migration fails. SQLite transactions are disabled by default. Do not mix `push` mode and migrations on the same database. Keep schema-affecting config the same across environments when generating migrations.

Pass `req` to Local API calls inside migrations so they share the transaction.

`migrate:status` lists which migrations have run.

## Checked

2026-11-04. Read database/migrations in the payloadcms/payload docs. Confirmed: script setup, migrationDir default, up/down signature, commands, when migrations are needed, prodMigrations and its cold-start warning, passing req. Clarified: --skip-empty, failure behaviour, SQLite transactions, push versus migrations.
Method: documentation only; no commands were run.
