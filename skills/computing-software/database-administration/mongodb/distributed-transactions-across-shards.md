---
id: computing-software.database-administration.mongodb.distributed-transactions-across-shards
name: distributed-transactions-across-shards
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, distributed-transactions, sharded-transactions, mongodb-transactions, two-phase-commit]
level: practitioner
status: docs-checked
description: "Run multi-document transactions across MongoDB shards: two-phase commit coordination, limits, performance costs, and designing to keep transactions single-shard."
sources:
  - https://www.mongodb.com/docs/manual/core/transactions-sharded-clusters/
  - https://www.mongodb.com/docs/manual/core/transactions-production-consideration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed transactions across shards

**Goal:** know what a cross-shard transaction costs and how to avoid needing one.

## How it works
- Transactions that target a single shard perform like replica set transactions; transactions that affect multiple shards incur a greater performance cost. The commit type is reported by `mongos` (`noShards`, `singleShard`, `singleWriteShard`, `readOnly`, `twoPhaseCommit`, `recoverWithToken`).
- Read concern `snapshot` is the only read concern that gives a consistent snapshot across multiple shards.
- A multi-shard transaction errors and aborts if any involved shard contains an arbiter.

## Limits and settings
- `transactionLifetimeLimitSeconds`: transactions run for less than one minute by default; longer ones expire and are aborted. On a sharded cluster change it on all shard replica set members. You can also set `maxTimeMS` on `commitTransaction` (capped by the lifetime limit).
- MongoDB writes as many oplog entries as needed per transaction, so the 16 MB total size limit is gone, but each oplog entry must still fit the 16 MB BSON limit.
- Abort abandoned transactions and abort and retry on errors, to limit WiredTiger cache pressure.
- Chunk migration takes exclusive collection locks at certain stages, so it waits for in-progress transactions on the collection; if a migration interleaves with a transaction (migration completes before the transaction takes its lock), the transaction errors at commit and aborts. Retry the transaction (for example with the driver's transaction helper).

## Costs
- Extra round trips for multi-shard commits and majority write concern on the participants.
- Transactions wait up to 5 ms for locks by default (`maxTransactionLockRequestTimeoutMillis`) and abort if they cannot get them.

## Design to avoid
- Pick shard keys so related documents (an order and its items) share a key prefix and land on one shard: `{ customerId: 1, ... }`.
- Embed related data in one document; single-document writes are atomic without transactions.
- Use outbox/sagas for workflows spanning services.

## Monitor
```javascript
db.serverStatus().transactions   // on mongos: totalStarted, totalCommitted, totalAborted, abortCause, commitTypes
```
`commitTypes.twoPhaseCommit` versus `singleShard` (mongos only) shows how many transactions are cross-shard.

## Verify
Load test the hot workflow; compare p99 for single-shard vs two-phase commits and watch `totalAborted` and `abortCause`.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: single-shard transactions perform like replica set transactions and multi-shard ones cost more, snapshot read concern is the only level giving a cross-shard snapshot, arbiter in an involved shard aborts multi-shard transactions, transactionLifetimeLimitSeconds (default under one minute, set on all shard members) and maxTimeMS on commitTransaction, oplog entries split with each entry within 16 MB, chunk migration waits for transaction locks and an interleaving migration aborts the transaction at commit, 5 ms lock wait and maxTransactionLockRequestTimeoutMillis, serverStatus transactions.commitTypes (mongos only) with twoPhaseCommit and singleShard. Removed the coordinator/prepare mechanics, 1,000-document guideline, DDL abort and version-gate claims that the manual pages do not state.

Method: documentation only; no commands were run.
