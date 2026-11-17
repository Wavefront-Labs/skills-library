---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-sort-key-patterns
name: dynamodb-sort-key-patterns
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-sort-key-patterns, dynamodb-keys, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Use composite sort keys to model hierarchies and range queries in one query."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sort key patterns

**Goal:** Use composite sort keys to model hierarchies and range queries in one query.

## Steps
- Query supports =, <, <=, >, >=, BETWEEN and begins_with on the sort key only.
- Hierarchical key: sk = "COUNTRY#AU#STATE#NSW#CITY#Sydney", then begins_with(sk, "COUNTRY#AU#STATE#NSW").
- ISO 8601 timestamps sort lexicographically, so use them for time ranges; ScanIndexForward=false returns newest first.
- Use Limit and LastEvaluatedKey for pagination; each Query page returns at most 1 MB.

## Gotcha
Numbers stored as strings sort lexicographically ("10" before "9"); zero-pad them or store type N.

## Verify
- [ ] A begins_with query returns only the intended slice, in the expected order, and consumes capacity only for matching items.
