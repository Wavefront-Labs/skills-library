---
id: computing-software.web-development.payload-cms.sqlite-adapter
name: sqlite-adapter
category: computing-software
field: web-development
product: payload-cms
tags: [sqlite, sqliteadapter, libsql-turso, wal-mode]
level: practitioner
status: docs-checked
description: "Configure sqliteAdapter with a libSQL client, WAL mode, busyTimeout, autoIncrement, blocksAsJSON and direct Drizzle access."
sources:
  - https://payloadcms.com/docs/database/sqlite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SQLite adapter

Goal: run Payload on SQLite or Turso.

```ts
import { sqliteAdapter } from '@payloadcms/db-sqlite'

export default buildConfig({
  db: sqliteAdapter({
    client: {
      url: process.env.DATABASE_URL,
      authToken: process.env.DATABASE_AUTH_TOKEN,
    },
  }),
})
```

Options: `client` (required, libSQL `createClient` options), `push`, `migrationDir`, `logger`, `idType` (`number` or `uuid`), `transactionOptions`, `localesSuffix`, `relationshipsSuffix`, `versionsSuffix`, `beforeSchemaInit`, `afterSchemaInit`, `generateSchemaOutputFile`, `autoIncrement`, `allowIDOnCreate`, `blocksAsJSON` (store blocks as a JSON column for performance with many blocks), `busyTimeout` (ms, default 0) and `wal` (Write-Ahead Logging for performance and concurrency).

Drizzle access:

```bash
npx payload generate:db-schema
```

```ts
import { eq, sql, and } from '@payloadcms/db-sqlite/drizzle'
const rows = await payload.db.drizzle.query.posts.findMany()
```

Migrations on SQLite use `db.run(sql\`...\`)` from `MigrateUpArgs`.

Verify: the database file or Turso database contains tables named after collection slugs.

## Checked

2026-11-04. Read database/sqlite and database/migrations. Confirmed: sqliteAdapter with client url and authToken, every listed option (client required, push, migrationDir, logger, idType number or uuid, transactionOptions, localesSuffix, relationshipsSuffix, versionsSuffix, beforeSchemaInit, afterSchemaInit, generateSchemaOutputFile, autoIncrement, allowIDOnCreate, blocksAsJSON, busyTimeout default 0, wal), payload generate:db-schema, the @payloadcms/db-sqlite/drizzle re-export, payload.db.drizzle queries, and db.run(sql`...`) in SQLite migrations.
Method: documentation only; no commands were run.
