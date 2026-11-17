---
id: computing-software.web-development.strapi.database-migrations
name: database-migrations
category: computing-software
field: web-development
product: strapi
tags: [strapi, database, migrations, knex, schema-sync, forcemigration]
level: advanced
status: docs-checked
description: "Write Strapi database migration files with knex: location, naming, run order, and what the schema sync does afterwards."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/database-migrations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database migrations

Experimental feature. Migration files live in `./database/migrations` and are named like `2022.05.10T00.00.00.name-of-my-migration.js`.

## Rules
- Each file runs once, in alphabetical order, before the automatic schema sync.
- Each migration runs inside its own transaction.
- Only `up` exists: no down migrations, and no CLI command to run them.
- The schema sync afterwards drops tables and columns that no longer match the content-types. Setting `forceMigration: false` in the database config skips those drops.

## Template
```js
'use strict';

async function up(knex) {}

module.exports = { up };
```

`knex` is the Knex instance, so use its schema builder or raw queries for data moves (for example copy a column before the sync drops it).

- A migration that uses the Strapi instance (for example `strapi.documents(...)`) instead of Knex must wrap its code in `strapi.db.transaction()`, otherwise a failure may not roll back.
- For TypeScript migrations set `settings.useTypescriptMigrations: true` in the database config so Strapi looks in the build directory; `allowJs: true` in `tsconfig.json` keeps existing JavaScript migrations working.
- `settings.runMigrations` controls only whether your own migration files run.

Config options live in `computing-software.web-development.strapi.database-config-file`.

## Checked

2026-11-04: checked against the Strapi docs page Database migrations (database-migrations) and the settings table of Database configuration. Confirmed: experimental status, folder and file naming, once-only alphabetical execution before the schema sync, one transaction per migration, no down migrations and no CLI, data loss during the sync, `forceMigration: false` skipping drops, the template and the Knex instance. Added from the page: the `strapi.db.transaction()` requirement, TypeScript migrations and `runMigrations`.

Method: documentation only; no commands were run.
