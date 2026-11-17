---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-global-tables-conflict-resolution
name: dynamodb-global-tables-conflict-resolution
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-global-tables-conflict-resolution, dynamodb-global-tables, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Design for last-writer-wins conflicts."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Global tables conflict resolution

**Goal:** Design for last-writer-wins conflicts.

## Steps
- Concurrent writes to the same item in different regions resolve by last writer wins using timestamps.
- Strongly consistent reads are consistent only within the writing region.
- Reduce conflicts by routing each item or user to one home region, and use conditional writes locally.
- Transactions are atomic only in the region where they run, not across replicas.

## Gotcha
Counters incremented in two regions can lose updates; use per-region counters summed on read.

## Verify
- [ ] A two-region concurrent write test behaves as documented and the design sends a key's writes to one region.
