---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-partiql-statements
name: dynamodb-partiql-statements
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-partiql-statements, dynamodb-partiql-queries, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Run SQL-compatible statements against DynamoDB tables."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PartiQL statements

**Goal:** Run SQL-compatible statements against DynamoDB tables.

## Steps
- aws dynamodb execute-statement --statement "SELECT * FROM \"Orders\" WHERE pk = ?" --parameters '[{"S":"CUSTOMER#42"}]'
- INSERT, UPDATE, DELETE and SELECT are supported; use ExecuteTransaction and BatchExecuteStatement for multiples.
- A SELECT without partition key equality (or IN) in the WHERE clause runs as a full table scan; deny it in IAM with the dynamodb:FullTableScan condition key.
- Query an index with FROM "Orders"."gsi1" (quoted names).

## Gotcha
PartiQL hides Scans behind SQL familiarity; check ConsumedCapacity.

## Verify
- [ ] The statement uses the intended key condition and ConsumedCapacity matches a Query, not a Scan.

## Checked
Checked 2026-11-03 against the PartiQL reference pages and botocore (ExecuteStatement Statement and Parameters): supported statement types, full-scan behaviour without partition key equality, the dynamodb:FullTableScan condition key and the quoted index syntax match. Replaced the begins_with example (not shown on the pages read) with a partition key equality query; resolved the FullTableScan "(confirm)".
Method: documentation only; no commands were run.
