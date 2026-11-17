---
id: computing-software.web-development.payload-cms.database-transactions
name: database-transactions
category: computing-software
field: web-development
product: payload-cms
tags: [transactions, begintransaction, req-in-hooks, rollback]
level: advanced
status: docs-checked
description: "Keep hook writes atomic by passing req to Local API calls and manage manual transactions with beginTransaction, commitTransaction and rollbackTransaction."
sources:
  - https://payloadcms.com/docs/database/transactions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transactions

Goal: make multi-step writes atomic.

By default Payload uses a transaction for data-changing operations when the database supports them (MongoDB needs a replica set; SQLite transactions are off by default and need `transactionOptions: {}`). Inside hooks, pass `req` to nested Local API calls so they join it:

```ts
const afterChange: CollectionAfterChangeHook = async ({ req }) => {
  await req.payload.create({ req, collection: 'my-slug', overrideAccess: true, data: { some: 'data' } })
}
```

Omit `req` and the nested call runs in its own transaction; if the outer one rolls back, it is not undone.

Async hooks: a non-awaited call that uses `req` is dangerous because the transaction may commit or roll back first; a non-awaited call without `req` is safely independent.

Direct control (for scripts):

- `payload.db.beginTransaction()` returns a transaction ID.
- `payload.db.commitTransaction(id)` finalises it.
- `payload.db.rollbackTransaction(id)` discards it.

```ts
const transactionID = await payload.db.beginTransaction()
try {
  await payload.create({ collection: 'posts', data, req: { transactionID } })
  await payload.db.commitTransaction(transactionID)
} catch (e) {
  await payload.db.rollbackTransaction(transactionID)
}
```

Adapters accept `transactionOptions` (or `false` to disable). Local API calls take `disableTransaction: true`.

## Checked

2026-11-04. Read database/transactions in the payloadcms/payload docs. Confirmed: passing req, un-awaited call danger, begin/commit/rollback methods, transactionOptions, disableTransaction. Fixed: transactions are not simply one per request; they apply to data-changing operations where the database supports them. Added: MongoDB replica set and SQLite notes. Removed: the verify step.
Method: documentation only; no commands were run.
