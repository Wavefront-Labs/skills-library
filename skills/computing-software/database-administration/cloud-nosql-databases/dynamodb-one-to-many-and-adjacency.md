---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-one-to-many-and-adjacency
name: dynamodb-one-to-many-and-adjacency
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-one-to-many-and-adjacency, dynamodb-single-table, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Store related items in one item collection so one Query returns a parent and its children."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# One-to-many and adjacency lists

**Goal:** Store related items in one item collection so one Query returns a parent and its children.

## Steps
- One-to-many: pk = CUSTOMER#42; sk = CUSTOMER#42 for the profile and ORDER#2026-11-02#9 for orders; Query on pk returns both.
- Many-to-many via adjacency list: items (pk=A, sk=B) and their inverse (pk=B, sk=A), or a GSI with swapped keys.
- Denormalise display attributes that rarely change; update copies with a transaction or a stream-driven job.
- Use a type attribute on each item so the application can decode it.

## Gotcha
A very large item collection makes pagination heavy, and with an LSI the collection is capped at 10 GB.

## Verify
- [ ] One Query retrieves the parent and its children, and reverse lookups work through the inverse item or GSI.
