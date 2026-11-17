---
id: computing-software.web-development.payload-cms.mongodb-adapter
name: mongodb-adapter
category: computing-software
field: web-development
product: payload-cms
tags: [mongodb, mongooseadapter, cosmosdb, compatibilityoptions]
level: practitioner
status: docs-checked
description: "Configure mongooseAdapter, its options (connectOptions, transactionOptions, collation) and compatibility presets for Firestore or Cosmos DB."
sources:
  - https://payloadcms.com/docs/database/mongodb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MongoDB adapter

Goal: run Payload on MongoDB.

```ts
import { mongooseAdapter } from '@payloadcms/db-mongodb'

export default buildConfig({
  db: mongooseAdapter({ url: process.env.DATABASE_URL }),
})
```

Options: `autoPluralization`, `bulkOperationsSingleTransaction`, `connectOptions`, `collectionsSchemaOptions`, `disableIndexHints`, `migrationDir`, `transactionOptions` (object or `false`), `collation` (MongoDB 3.4+, default locale `en`), `allowAdditionalKeys` (by default keys not in the schema are stripped), `allowIDOnCreate`, `disableFallbackSort`, `useAlternativeDropDatabase`, `useBigIntForNumberIDs`, `useJoinAggregations`, `usePipelineInSortLookup`.

Access Mongoose models: `payload.db.collections[slug]`, `payload.db.globals`, `payload.db.versions[slug]`.

Other MongoDB-compatible services:

```ts
import { mongooseAdapter, compatibilityOptions } from '@payloadcms/db-mongodb'
db: mongooseAdapter({ url: process.env.DATABASE_URL, ...compatibilityOptions.firestore })
```

`compatibilityOptions` exports recommended settings for DocumentDB, Azure Cosmos DB and Firestore; these databases are not officially supported, so expect some issues. Azure Cosmos DB does not support transactions that update documents in different collections (common with hooks) and also needs the root config property `indexSortableFields: true`. Look up the exact values inside `compatibilityOptions` in the package rather than copying them.

Verify: documents appear in the expected MongoDB collections.

## Checked

2026-11-04. Read database/mongodb. Confirmed: the mongooseAdapter option list (autoPluralization, bulkOperationsSingleTransaction, connectOptions, collectionsSchemaOptions, disableIndexHints, migrationDir, transactionOptions, collation with MongoDB 3.4+ and default locale en, allowAdditionalKeys, allowIDOnCreate, disableFallbackSort, useAlternativeDropDatabase, useBigIntForNumberIDs, useJoinAggregations, usePipelineInSortLookup), the Mongoose model accessors, and compatibilityOptions for DocumentDB, Cosmos DB and Firestore. Removed: the specific option values claimed for compatibilityOptions.cosmosdb (the page does not list them). Kept: the Cosmos DB transaction limitation and indexSortableFields requirement, both on the page.
Method: documentation only; no commands were run.
