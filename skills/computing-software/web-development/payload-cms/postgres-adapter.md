---
id: computing-software.web-development.payload-cms.postgres-adapter
name: postgres-adapter
category: computing-software
field: web-development
product: payload-cms
tags: [postgres, postgresadapter, drizzle-push, read-replicas]
level: practitioner
status: docs-checked
description: "Configure postgresAdapter with pool, push, schemaName, idType, migrationDir, suffix options and read replicas."
sources:
  - https://payloadcms.com/docs/database/postgres
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Postgres adapter

Goal: run Payload on PostgreSQL.

```ts
import { postgresAdapter } from '@payloadcms/db-postgres'

export default buildConfig({
  db: postgresAdapter({
    pool: { connectionString: process.env.DATABASE_URL },
  }),
})
```

On Vercel use `vercelPostgresAdapter()` from `@payloadcms/db-vercel-postgres`.

Options: `pool` (required, node-postgres pool options), `push` (Drizzle db push, enabled in development only by default), `extensions` (for example `['unaccent']`), `query.operatorHandlers`, `migrationDir`, `schemaName` (experimental, default `public`), `idType` (`serial` or `uuid`), `transactionOptions` (or `false` to disable), `disableCreateDatabase`, `localesSuffix` (`_locales`), `relationshipsSuffix` (`_rels`), `versionsSuffix` (`_v`), `beforeSchemaInit`, `afterSchemaInit`, `generateSchemaOutputFile`, `allowIDOnCreate`, `readReplicas`, `readReplicasAfterWriteInterval`.

- `readReplicas` offloads reads; `readReplicasAfterWriteInterval` (ms, default 2000, `0` disables) keeps reads on the primary after a write to avoid stale reads.
- Dev uses `push` to sync schema automatically and warns when changes would lose data; disable it to rely on migrations only.

Verify: `pnpm payload generate:db-schema` writes the Drizzle schema.

## Checked

2026-11-04. Read database/postgres. Confirmed: the postgresAdapter pool example, vercelPostgresAdapter from @payloadcms/db-vercel-postgres, every option in the skill (pool required, push default development only, extensions with query.operatorHandlers, migrationDir, schemaName experimental default public, idType serial or uuid, transactionOptions or false, disableCreateDatabase, localesSuffix, relationshipsSuffix, versionsSuffix, beforeSchemaInit, afterSchemaInit, generateSchemaOutputFile, allowIDOnCreate, readReplicas, readReplicasAfterWriteInterval), the push data-loss warning, and payload generate:db-schema. Added: the 2000 ms default.
Method: documentation only; no commands were run.
