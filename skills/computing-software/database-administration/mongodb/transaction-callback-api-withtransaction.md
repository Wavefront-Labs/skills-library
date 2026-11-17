---
id: computing-software.database-administration.mongodb.transaction-callback-api-withtransaction
name: transaction-callback-api-withtransaction
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-transactions, withtransaction, core-api, transient-transaction-error, unknown-transaction-commit-result]
level: practitioner
status: docs-checked
description: "Write MongoDB multi-document transactions with the callback API (withTransaction) that retries correctly, versus the core API where you must handle retry labels yourself."
sources:
  - https://www.mongodb.com/docs/manual/core/transactions-in-applications/
  - https://www.mongodb.com/docs/manual/core/transactions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions: callback API vs core API

## Callback API (use this)
The driver starts the transaction, runs your function, commits, and **retries** the whole
function on `TransientTransactionError` and the commit on `UnknownTransactionCommitResult`.
```js
// Node.js driver
const session = client.startSession();
try {
  await session.withTransaction(async () => {
    const accounts = client.db("bank").collection("accounts");
    await accounts.updateOne({ _id: "A" }, { $inc: { balance: -100 } }, { session });
    await accounts.updateOne({ _id: "B" }, { $inc: { balance: 100 } }, { session });
  }, {
    readConcern: { level: "snapshot" },
    writeConcern: { w: "majority" },
    readPreference: "primary"
  });
} finally {
  await session.endSession();
}
```
Other drivers expose the same callback API; see the driver documentation.

Rules for the callback:
- Pass `session` to **every** operation inside, or that operation runs outside the transaction.
- The function may run more than once: no side effects outside the database (sending emails,
  publishing messages) inside it. Do those after it returns.
- Keep it short; long-running transactions are aborted by the server's transaction time limits.

## Core API (manual control)
```js
session.startTransaction({ readConcern: { level: "snapshot" }, writeConcern: { w: "majority" } });
try {
  // ... operations with { session }
  await commitWithRetry(session);
} catch (e) {
  await session.abortTransaction();
  // if e carries the TransientTransactionError label, retry the whole transaction
  throw e;
}
```
You must implement: retry of the entire transaction on `TransientTransactionError` and retry of **commit only** on `UnknownTransactionCommitResult`
(the commit may have succeeded). Use it only when you need custom control flow.

## Settings that matter
- `writeConcern: majority` for durability across failover; `readConcern: snapshot` for a
  consistent view.
- Transactions that contain reads must use read preference `primary`.
- Design to touch fewer hot documents; write conflicts are likelier under contention.

## Gotchas
- You can create collections and indexes in transactions, with restrictions (for example, not new collections in cross-shard write transactions).
- Since 6.2 the server does not retry a transaction that fails with `TransactionTooLargeForCache`; split large work.

## Verify
In a test, kill/step down the primary mid-transaction: the callback-API code completes once
(no duplicate effect) after retry; logs show the retry on `TransientTransactionError`.

## Checked

2026-10-28. Confirmed against MongoDB manual transactions pages: callback API retries TransientTransactionError and UnknownTransactionCommitResult, core API leaves retry to the application, commit retry only for UnknownTransactionCommitResult, reads need read preference primary, create collections and indexes in transactions with the cross-shard restriction, TransactionTooLargeForCache not retried since 6.2, majority write concern. Removed unconfirmed: the 120 s and 60 s limits, WriteConflict code 112, Python call signature, 4.4+ tag, replica-set-only note.

Method: documentation only; no commands were run.
