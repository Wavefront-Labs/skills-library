---
id: computing-software.web-development.drizzle-orm.drizzle-kit-migrate-apply
name: drizzle-kit-migrate-apply
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, migrate, migrations-table, deployment]
level: practitioner
status: docs-checked
description: "Apply generated SQL with drizzle-kit migrate or the runtime migrate() helper, and understand the migrations log table in the drizzle schema."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-migrate.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/migrations.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply pending migrations safely.

`drizzle-kit migrate` reads the migration folders, fetches the applied-migrations log from the database, selects migrations not yet applied, runs them and records them. It needs `dialect` and `dbCredentials`.

```sh
npx drizzle-kit migrate
npx drizzle-kit migrate --dialect=postgresql --url=postgresql://user:password@host:port/dbname
```

The log table is `__drizzle_migrations` in schema `drizzle` by default; change with `migrations: { table: 'journal', schema: 'drizzle' }` in the config.

Runtime alternative (flow 4 in the docs):

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
const db = drizzle(process.env.DATABASE_URL);
await migrate(db);
```

The migrator import path depends on the driver. The docs say this approach is widely used for monolithic applications applying migrations during zero-downtime deployment (rolling back DDL changes if something fails), and in serverless deployments with migrations running in a custom resource once during deployment.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-kit-migrate.mdx, migrations.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
