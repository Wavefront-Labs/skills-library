---
id: computing-software.web-development.payload-cms.database-adapters
name: database-adapters
category: computing-software
field: web-development
product: payload-cms
tags: [database-adapters, mongodb-vs-postgres, db-batchprocessing, drizzle]
level: practitioner
status: docs-checked
description: "Choose between the MongoDB (Mongoose), Postgres and SQLite (Drizzle) adapters and use batch processing."
sources:
  - https://payloadcms.com/docs/database/overview
  - https://payloadcms.com/docs/database/postgres
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database adapters

Goal: pick and configure a database adapter.

Official adapters: `@payloadcms/db-mongodb` (Mongoose), `@payloadcms/db-postgres` (Drizzle) and `@payloadcms/db-sqlite` (Drizzle), plus `@payloadcms/db-vercel-postgres`.

```ts
import { mongooseAdapter } from '@payloadcms/db-mongodb'
export default buildConfig({
  db: mongooseAdapter({ url: process.env.DATABASE_URL }),
})
```

Choose non-relational (MongoDB) when you prefer simplicity, do not want to keep environments in sync with DDL changes, localize most content, or use many arrays, blocks or `hasMany` selects. Choose relational (Postgres or SQLite) when you are comfortable with migrations, need database-enforced consistency, or have many enforced relationships.

Batch processing helper:

```ts
await payload.db.batchProcessing({
  batchSize: 100,
  operations: [
    { operation: 'create', args: { collection: 'posts', data: { title: 'Created in a batch' } } },
  ],
  req,
})
```

`batchProcessing` runs `create`, `updateOne` and `deleteOne` operations in order, stops at the first failure unless `shouldContinueOnError` is set, does not manage transactions, and bypasses access control, hooks and validation. `@payloadcms/db-vercel-postgres` is documented on the Postgres page. SQLite has no Point field.

Adapter-specific options live on each adapter page (`migrationDir`, `transactionOptions`, `allowIDOnCreate`, `idType`).

## Checked

2026-11-04. Read database/overview, database/postgres, database/sqlite and database/mongodb in the payloadcms/payload docs. Confirmed: adapter packages, relational versus non-relational guidance, the listed adapter options. Added: batchProcessing details, SQLite Point limitation, Postgres page as a source. Removed: the unconfirmed verify step.
Method: documentation only; no commands were run.
