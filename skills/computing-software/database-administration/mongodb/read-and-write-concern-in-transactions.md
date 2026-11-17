---
id: computing-software.database-administration.mongodb.read-and-write-concern-in-transactions
name: read-and-write-concern-in-transactions
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, transaction-read-concern, transaction-write-concern, mongodb-transactions, snapshot-read]
level: practitioner
status: docs-checked
description: "Pick read concern, write concern and read preference for MongoDB transactions, and understand what snapshot, majority and local mean for visibility and durability."
sources:
  - https://www.mongodb.com/docs/manual/core/transactions/#read-concern-write-concern-read-preference
  - https://www.mongodb.com/docs/manual/reference/read-concern-snapshot/
  - https://www.mongodb.com/docs/manual/reference/write-concern/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read and write concern inside transactions

**Goal:** set concerns at the **transaction** level (not per operation) so reads see a consistent snapshot and commits are durable.

## Rules
- Set read concern at the transaction level, not on individual operations; use `startTransaction` or the session defaults.
- Transactions that contain reads must use read preference `primary`.

```javascript
session.startTransaction({
  readConcern: { level: "snapshot" },
  writeConcern: { w: "majority", wtimeout: 5000 },
  readPreference: "primary"
})
```

## Read concern options
| Level | Meaning in a transaction |
|---|---|
| `local` | On sharded clusters it cannot guarantee data from the same snapshot across shards |
| `majority` | Majority-committed data if the transaction commits with `w: "majority"`; cannot guarantee a same-snapshot view across shards |
| `snapshot` | On sharded clusters the snapshot view is synchronized across shards |
Use `snapshot` when multi-shard reads must agree (balances, inventory).

## Write concern
- `w: "majority"` acknowledges after the commit has been applied to a majority of voting members.
- On `UnknownTransactionCommitResult`, retry the commit operation rather than re-running the whole transaction (the callback API does this for you).

## Causal consistency
Causal consistency guarantees for `majority` reads and `majority` writes in a causally consistent session hold across all members of the deployment; read preference does not affect them.

## Verify
In a test, run a transaction with `snapshot` reading two shards while a concurrent writer updates both; results must be from a single point in time.

## Checked

2026-10-28. Confirmed against MongoDB manual transactions, read concern snapshot, write concern and read preference pages: read concern set at the transaction level, read preference primary for reads in transactions, local and majority cannot guarantee a same-snapshot view across shards while snapshot is synchronized across shards, w majority acknowledgment, commit retry on UnknownTransactionCommitResult, causal consistency with majority concerns. Removed unconfirmed: the claim that per-operation concerns are ignored, the 'commit cannot be rolled back' wording, the default-sessions-causal statement, the local default and speed advice.

Method: documentation only; no commands were run.
