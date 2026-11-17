---
id: computing-software.database-administration.mongodb.transaction-error-labels-and-retry
name: transaction-error-labels-and-retry
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-transactions, multi-document-transactions, transient-transaction-error, unknown-transaction-commit-result, with-transaction, retryable-writes, write-conflict]
level: advanced
status: docs-checked
description: "Write MongoDB multi-document transactions that survive elections and write conflicts: withTransaction, TransientTransactionError and UnknownTransactionCommitResult retries."
sources:
  - https://www.mongodb.com/docs/manual/core/transactions-in-applications/
  - https://www.mongodb.com/docs/manual/core/transactions-production-consideration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions: error labels and retry

**Goal:** transactions that commit exactly once despite failovers and conflicts.

## Use the callback API
Drivers' callback API (`withTransaction` in most drivers) has the retry logic built in: it retries the whole transaction on `TransientTransactionError` and retries the commit on `UnknownTransactionCommitResult`:
```javascript
const session = client.startSession();
try {
  await session.withTransaction(async () => {
    await accounts.updateOne({ _id: from }, { $inc: { balance: -amt } }, { session });
    await accounts.updateOne({ _id: to },   { $inc: { balance:  amt } }, { session });
  }, { readConcern: { level: "snapshot" }, writeConcern: { w: "majority" } });
} finally { await session.endSession(); }
```
Every operation must pass `{ session }`; one forgotten option runs outside the transaction.

## What the labels mean (core API, if you handle it yourself)
The core API has no retry logic; the application must add it.
- **TransientTransactionError**: an operation in the transaction returned this label (for example the primary stepped down), so the transaction as a whole can be retried from the start. Individual writes inside a transaction are not retryable, whatever `retryWrites` says.
- **UnknownTransactionCommitResult**: the commit returned this label, so the commit can be retried. Commits are retryable write operations, and drivers retry a failing commit regardless of `retryWrites`.
- Errors without these labels (validation error, duplicate key) are application errors: do not retry blindly.

## Write conflicts
If a write outside the transaction modifies a document that an operation in the transaction later tries to modify, the transaction aborts with a write conflict; conversely, an outside write to a document the transaction already modified gets a write conflict error. An uncommitted transaction that puts excessive pressure on the WiredTiger cache also aborts with a write conflict error. Hot documents (counters, one shared "inventory" document) cause retry storms: restructure the data rather than retrying harder.

## Gotchas
- Transactions must run for less than one minute by default (`transactionLifetimeLimitSeconds` on every `mongod`, and on all shard replica set members in a sharded cluster); a periodic cleanup aborts expired ones, which also relieves cache pressure. Keep transactions short and small.
- Use `w: "majority"` write concern for the transaction (set in the transaction options at start or in the callback options).
- Transactions cannot run on a sharded cluster with a shard where `writeConcernMajorityJournalDefault` is false.

## Verify
Fault test: run a loop of transactions and `rs.stepDown()` the primary; no duplicate or lost transfers (sum of balances unchanged).

## Checked
2026-10-31. Against the MongoDB manual pages Transactions in Applications and Production Considerations: callback vs core API retry behaviour, both error labels, retryable commit, write conflict behaviour, one-minute default and `transactionLifetimeLimitSeconds`, cache pressure abort, `writeConcernMajorityJournalDefault` sharding restriction. Removed unconfirmed details: "commit is idempotent", the immediate-WriteConflict-labelled-transient claim, `db.serverStatus().transactions` fields, and the `retryWrites=true` default remark.
Method: documentation only; no commands were run.
