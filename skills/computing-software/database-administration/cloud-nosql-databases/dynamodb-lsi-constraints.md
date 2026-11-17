---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-lsi-constraints
name: dynamodb-lsi-constraints
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-lsi-constraints, dynamodb-indexes, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use an LSI only when you need a second sort order within the same partition key and strong consistency."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local secondary index constraints

**Goal:** Use an LSI only when you need a second sort order within the same partition key and strong consistency.

## Steps
- LSIs must be created at table creation time; they cannot be added or removed later.
- They share the base table's throughput and allow strongly consistent reads.
- A table with an LSI has a 10 GB limit per partition key value (item collection size limit).
- Maximum 5 LSIs per table.

## Gotcha
The 10 GB item-collection cap causes ItemCollectionSizeLimitExceededException on writes; prefer a GSI unless you truly need strong consistency.

## Verify
- [ ] describe-table lists the LocalSecondaryIndexes and monitoring shows item collection sizes far below 10 GB.

## Checked
Checked 2026-11-03 against the secondary index, item collection and service quotas pages and botocore (ItemCollectionSizeLimitExceededException is a documented write error): creation only at table creation, shared throughput, strong consistency, 10 GB per partition key value and the 5 index limit match. Resolved the "(confirm)" on the LSI count.
Method: documentation only; no commands were run.
