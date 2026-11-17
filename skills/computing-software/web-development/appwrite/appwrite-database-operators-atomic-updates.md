---
id: computing-software.web-development.appwrite.appwrite-database-operators-atomic-updates
name: appwrite-database-operators-atomic-updates
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, operators, atomic, concurrency, tablesdb]
level: advanced
status: docs-checked
description: "Update fields atomically on the server with Operator helpers for numbers, arrays, strings and dates instead of read-modify-write."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/operators/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid lost updates under concurrency.

Pass an operator as the field value in an update or upsert: `tablesDB.updateRow({ databaseId, tableId, rowId, data: { letters: Operator.arrayAppend(['c']) } })`. The server applies it atomically and operators can be staged inside transactions.

Operators documented (each updates its column atomically on the server):
- Numeric: `increment`, `decrement`, `multiply`, `divide`, `modulo`, `power`. Increment, multiply and power can cap the result at a maximum; decrement and divide at a minimum. The divisor cannot be zero.
- Arrays: `arrayAppend(['c'])`, `arrayPrepend`, `arrayInsert(1, 'x')` (insert at an index), `arrayRemove('b')`, `arrayUnique()`, `arrayIntersect`, `arrayDiff` (elements in the current array but not in the provided one), `arrayFilter(Condition.GreaterThan, 10)`.
- Strings: `stringConcat` (to a string or array field), `stringReplace('old', 'new')`.
- Boolean: `toggle`.
- Dates: `dateAddDays(7)`, `dateSubDays(3)`, `dateSetNow()` (current server time).

Use when updating likes, scores, credits or inventory, editing tags without rewriting arrays, or adjusting schedule dates. Multiple operators can hit different fields in one request.

Gotcha: operators replace the read-modify-write pattern (fetch, change client-side, write back), which is what loses updates under concurrency; do not fall back to it for fields that need atomic changes.

Transactions: operators can be staged and committed with other database actions, for example `updateRow` with a `transactionId`, or `createOperations` with `action: 'update'` entries.

Note: the server applies the operator and returns the new value, so the value you read before sending the request does not affect the result.


## Checked

2026-11-04. Confirmed against the Appwrite docs page Operators (databases/operators), read from the raw markdown because the rendered page was truncated: the `Operator` import and `updateRow` usage, the operator list per type with caps, the divisor rule, the transaction examples with `createOperations` and `transactionId`, and the use cases. Removed: the claim that column types must match the operator, which the page does not state, and the concurrency Verify test.
Method: documentation only; no commands were run.
