---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-transactwrite-items
name: dynamodb-transactwrite-items
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-transactwrite-items, dynamodb-transactions, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Make multi-item changes atomic and isolated."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TransactWriteItems and TransactGetItems

**Goal:** Make multi-item changes atomic and isolated.

## Steps
- TransactWriteItems supports Put, Update, Delete and ConditionCheck on up to 100 actions in one request, up to 4 MB total, across tables in the same account and Region.
- Each item costs two underlying reads or writes (prepare and commit).
- Use ClientRequestToken (up to 36 characters) for idempotency; the token is valid for 10 minutes.
- Failures return TransactionCanceledException with CancellationReasons per item, for example ConditionalCheckFailed or TransactionConflict.

## Gotcha
Two transactions touching the same item concurrently conflict; retry with backoff.

## Verify
- [ ] A test that violates one condition leaves all items unchanged and the cancellation reasons identify the failing item.

## Checked
Checked 2026-11-03 against the transactions page and botocore (TransactWriteItems, ClientRequestToken): 100 actions, 4 MB, same account and Region, two underlying operations per item, the 10 minute idempotency window and TransactGetItems limit match. Resolved the "(confirm)" on the item count and added the 36-character token limit.
Method: documentation only; no commands were run.
