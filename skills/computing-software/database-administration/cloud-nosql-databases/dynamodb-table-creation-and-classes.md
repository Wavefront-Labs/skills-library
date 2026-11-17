---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-table-creation-and-classes
name: dynamodb-table-creation-and-classes
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-table-creation-and-classes, dynamodb-tables, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Create a table with the right key schema, billing mode and table class from the start."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table creation and table classes

**Goal:** Create a table with the right key schema, billing mode and table class from the start.

## Steps
- aws dynamodb create-table --table-name Orders --attribute-definitions AttributeName=pk,AttributeType=S AttributeName=sk,AttributeType=S --key-schema AttributeName=pk,KeyType=HASH AttributeName=sk,KeyType=RANGE --billing-mode PAY_PER_REQUEST
- Table class is STANDARD or STANDARD_INFREQUENT_ACCESS; the docs suggest Standard-IA when storage costs exceed 50 percent of throughput costs.
- Enable deletion protection with --deletion-protection-enabled.

## Gotcha
The key schema and attribute types of the table cannot be changed after creation; a change means a new table and a data migration.

## Verify
- [ ] describe-table shows ACTIVE, expected KeySchema, BillingModeSummary, TableClassSummary and DeletionProtectionEnabled true.

## Checked
Checked 2026-11-03 against the table classes page and botocore CreateTable (AttributeDefinitions, KeySchema, BillingMode, TableClass, DeletionProtectionEnabled): the classes, the 50 percent storage guidance and the flag names match. Removed the unconfirmed price-direction statement and the tagging advice (resolved the "(confirm)"). The key-schema immutability gotcha is a standard DynamoDB property and UpdateTable has no key-schema parameter.
Method: documentation only; no commands were run.
