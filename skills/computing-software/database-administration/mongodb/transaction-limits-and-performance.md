---
id: computing-software.database-administration.mongodb.transaction-limits-and-performance
name: transaction-limits-and-performance
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-transactions, transaction-lifetime-limit, multi-document-transactions, maxtransactionlocktimeoutmillis, write-conflict, transaction-size, wiredtiger-cache-pressure]
level: practitioner
status: docs-checked
description: "Keep MongoDB multi-document transactions healthy: the lifetime limit, lock request timeout, oplog entry size, read and write concern, and design alternatives."
sources:
  - https://www.mongodb.com/docs/manual/core/transactions-production-consideration/
  - https://www.mongodb.com/docs/manual/reference/parameters/#mongodb-parameter-param.transactionLifetimeLimitSeconds
  - https://www.mongodb.com/docs/manual/core/transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction limits and performance

**Goal:** use transactions where atomicity across documents is needed without stalling the cluster.

## Limits and their parameters
| Limit | Default | Parameter |
|---|---|---|
| Runtime of a transaction | Less than one minute; expired transactions are aborted by a periodic cleanup | `transactionLifetimeLimitSeconds` (set on every shard replica set member in a sharded cluster) |
| Wait to acquire locks in a txn | 5 ms, then the transaction aborts | `maxTransactionLockRequestTimeoutMillis` (-1 gives an operation-specific timeout) |
| Oplog entries | A transaction creates as many oplog entries as needed; each entry must fit the 16 MB BSON document limit | - |

The lifetime limit also exists to relieve storage cache pressure: long transactions are a reason to redesign, not to raise the limit.
Raising `maxTransactionLockRequestTimeoutMillis` can avoid aborts on momentary lock contention (such as fast metadata operations) but can delay the abort of deadlocked transaction operations. A pending DDL operation that outlasts it aborts the transactions queued behind it.

## Design
- Keep transactions short: read, compute in the app before starting, write, commit.
- Do not do network calls / user think time inside.
- Batch large bulk changes outside transactions (idempotent upserts), not one giant txn.
- Prefer single-document atomicity by modelling (embed what changes together).

## Read and write concern
`session.startTransaction({ readConcern: { level: "snapshot" }, writeConcern: { w: "majority" } })`.
Read concern `"snapshot"` returns data from a snapshot of majority-committed data only if the transaction commits with `w: "majority"`. On sharded clusters, the `"snapshot"` view is synchronized across shards, but `"local"` and `"majority"` cannot guarantee a single snapshot view. When creating or dropping a collection just before a transaction that uses it, issue that DDL with write concern `"majority"`.

## Gotchas
- Transactions cannot write to capped collections or read/write collections in the `config`, `admin` or `local` databases.
- Transactions that exceed the lifetime limit are aborted.

## Verify
No transaction runs longer than expected in `currentOp`, and aborts stay a small fraction of commits under load (`db.serverStatus().transactions`).

## Checked
2026-10-31. Confirmed in the MongoDB manual pages for Transactions and Production Considerations:
the lifetime default (under one minute) and `transactionLifetimeLimitSeconds` scope, the 5 ms lock
timeout and `maxTransactionLockRequestTimeoutMillis` behaviour, oplog entry sizing, snapshot / majority
read concern and `w: "majority"` semantics, capped collection and `config` / `admin` / `local`
restrictions. Removed (not confirmed in the fetched pages): the ">1000 documents" guidance, the
`WriteConflict` retry description and `serverStatus` field list, cross-shard two-phase commit
wording, the DDL-in-transaction rule and `NoSuchTransaction` behaviour.
Method: documentation only; no commands were run.
