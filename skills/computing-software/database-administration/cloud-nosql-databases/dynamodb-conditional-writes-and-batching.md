---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-conditional-writes-and-batching
name: dynamodb-conditional-writes-and-batching
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-conditional-writes-and-batching, dynamodb-transactions, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use condition expressions for optimistic locking and batch calls for throughput."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional writes and batch operations

**Goal:** Use condition expressions for optimistic locking and batch calls for throughput.

## Steps
- PutItem with ConditionExpression attribute_not_exists(pk) prevents overwrite; UpdateItem with condition version = :v then SET version = version + 1 gives optimistic locking.
- BatchWriteItem takes up to 25 puts/deletes and 16 MB; BatchGetItem up to 100 items and 16 MB.
- Batch calls are not atomic and return UnprocessedItems/UnprocessedKeys; retry those with backoff.
- ReturnValuesOnConditionCheckFailure=ALL_OLD returns the existing item on failure.

## Gotcha
Batch operations cannot use condition expressions or updates; use TransactWriteItems or single calls.

## Verify
- [ ] Concurrent updates produce ConditionalCheckFailedException instead of lost updates and unprocessed items are retried to zero.

## Checked
Checked 2026-11-03 against the API reference pages and botocore: BatchWriteItem 25 puts/deletes and 16 MB with no UpdateItem, BatchGetItem 100 items and 16 MB, UnprocessedItems in the output, attribute_not_exists(pk) preventing overwrite and ReturnValuesOnConditionCheckFailure ALL_OLD (default NONE) match.
Method: documentation only; no commands were run.
