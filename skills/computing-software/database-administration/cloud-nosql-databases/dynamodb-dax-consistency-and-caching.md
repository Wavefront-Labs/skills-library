---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-dax-consistency-and-caching
name: dynamodb-dax-consistency-and-caching
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-dax-consistency-and-caching, dynamodb-dax, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Understand staleness and invalidation before putting DAX in production."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAX consistency and caching behaviour

**Goal:** Understand staleness and invalidation before putting DAX in production.

## Steps
- The item cache holds GetItem/BatchGetItem results; the query cache holds Query/Scan results separately and is not invalidated by item writes.
- Writes update the item cache only if they pass through DAX; writes direct to DynamoDB leave stale data until TTL.
- Use a short query TTL when queries must reflect writes (a query TTL of 0 means no caching). Both caches default to a 5 minute TTL.
- Strongly consistent reads and TransactGetItems pass through DAX uncached.

## Gotcha
Updating an item does not refresh cached query results, so list screens can show old data for the TTL.

## Verify
- [ ] A write-then-query test shows the expected staleness window and the application tolerates it.

## Checked
Checked 2026-11-03 against the DAX concepts and consistency pages: separate item and query caches, query cache not invalidated by item writes, writes outside DAX leaving stale data until TTL, 5 minute default TTLs and uncached strongly consistent reads match. Removed the unconfirmed "cache misses pay full read cost" line.
Method: documentation only; no commands were run.
