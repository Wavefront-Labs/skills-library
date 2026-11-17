---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-access-pattern-modelling
name: dynamodb-access-pattern-modelling
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-access-pattern-modelling, dynamodb-single-table, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Model from the list of queries, not from entities."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Access pattern modelling

**Goal:** Model from the list of queries, not from entities.

## Steps
- List every access pattern with its frequency and latency need; map each to a Query on a key or index.
- Draw an entity chart: for each entity define pk/sk templates, for example USER#id / PROFILE and USER#id / ORDER#ts.
- Reuse generic attribute names (pk, sk, gsi1pk, gsi1sk) so one table and few indexes serve many entity types.
- Overload GSI1 to serve a second lookup, for example gsi1pk = ORDER#id.

## Gotcha
A pattern missed at design time often needs a new GSI plus a backfill; review patterns with every stakeholder before building.

## Verify
- [ ] Every listed access pattern maps to one Query or GetItem with no Scan, documented in a pattern-to-key table.
