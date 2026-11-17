---
id: computing-software.database-administration.mongodb.refining-a-shard-key
name: refining-a-shard-key
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, refine-shard-key, mongodb-sharding, shard-key, jumbo-chunks]
level: practitioner
status: docs-checked
description: "Add suffix fields to an existing MongoDB shard key with refineCollectionShardKey (4.4+) to split jumbo chunks and improve distribution, without moving data."
sources:
  - https://www.mongodb.com/docs/manual/core/sharding-refine-a-shard-key/
  - https://www.mongodb.com/docs/manual/reference/command/refineCollectionShardKey/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refining a shard key

**Goal:** fix a low-cardinality shard key (e.g. `{ customerId: 1 }` where one customer is huge) by appending fields, so chunks can split.

## Refine vs reshard
`refineCollectionShardKey` only adds suffix fields to the existing key (the prefix stays) and can address jumbo chunks caused by insufficient cardinality. Changing the prefix needs a different tool (`reshardCollection`, not covered here).

## Steps
1. Create an index that supports the new key (the new key must be a prefix of it):
```javascript
db.orders.createIndex({ customerId: 1, orderId: 1 })
```
3. Refine:
```javascript
db.adminCommand({ refineCollectionShardKey: "shop.orders", key: { customerId: 1, orderId: 1 } })
```

## Gotchas
- If the current shard key index has a uniqueness constraint, the new shard key index must also be unique.
- The new key must be supported by an index that exists before you run the command.

## Verify
`sh.status()` shows the new shard key for the collection.

## Checked

2026-10-28. Confirmed against MongoDB manual refineCollectionShardKey command and Refine a Shard Key pages: the command adds suffix fields, the new key must be supported by a pre-existing index, a unique current index requires a unique new index, it can address jumbo chunks from low cardinality, sh.status() to verify. Removed unconfirmed: metadata-only and copy comparison, missing-value-as-null rule, clearJumboFlag step, upsert and zone and flushRouterConfig notes, config.collections check.

Method: documentation only; no commands were run.
