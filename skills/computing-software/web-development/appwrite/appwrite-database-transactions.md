---
id: computing-software.web-development.appwrite.appwrite-database-transactions
name: appwrite-database-transactions
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, transactions, atomicity, tablesdb]
level: advanced
status: docs-checked
description: "Stage multiple row operations across tables and commit or roll them back atomically with createTransaction and updateTransaction."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/transactions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: all-or-nothing changes across rows and tables.

Flow:
1. `createTransaction` returns a transaction with `$id`.
2. Stage work by passing `transactionId` to create, update, upsert, delete and atomic numeric methods, including their bulk versions (`createRows`, `updateRows`, `upsertRows`, `deleteRows`). Or stage many at once with `createOperations`, an array of objects `{ action, databaseId, tableId, rowId, data }` where `action` is one of `create`, `update`, `upsert`, `increment`, `decrement`, `delete`, `bulkCreate`, `bulkUpdate`, `bulkUpsert`, `bulkDelete`. For increment and decrement, `data` is `{ value, min, max, column }` (min and max optional); create, update and upsert take a raw data object; bulk update and delete take `queries`.
3. Call `updateTransaction({ transactionId, commit: true })` to commit, or `rollback: true` to roll back.

Behavior: staged operations are written to a staging area, so tables are untouched until commit. On commit, Appwrite replays the log in order inside a real database transaction; later staged steps see earlier ones. If an affected row changed outside the transaction, the commit fails with a conflict. Operations can span databases and tables. Schema operations such as adding columns are not included.

Plan limits for operations per transaction: Free 100, Pro 1,000, Scale 2,500.

Gotcha: if a row changed outside the transaction after it was staged, the commit fails with a conflict error. Resolve it, for example by refetching and re-staging, and try again. The docs advise keeping transactions short-lived and staging changes in the order they must be applied.

Atomic numeric methods can be staged too, for example `incrementRowColumn` with `transactionId`.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Transactions (databases/transactions), read from the raw markdown because the rendered page was truncated: the three-step flow, staging area, replay in order with read-your-own-writes, conflicts, cross-database scope, schema exclusion, plan limits (Free 100, Pro 1,000, Scale 2,500), the `createOperations` action list and data shapes, and commit and rollback calls. Replaced the generic retry advice with the page's refetch-and-re-stage advice; removed the rollback Verify step.
Method: documentation only; no commands were run.
