---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-multi-region-writes-and-conflicts
name: cosmos-multi-region-writes-and-conflicts
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-multi-region-writes-and-conflicts, cosmos-global-distribution, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Enable multi-region writes with a conflict policy."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/multi-region-writes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/conflict-resolution-policies
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-region writes and conflict resolution

**Goal:** Enable multi-region writes with a conflict policy.

## Steps
- Enable at account level: az cosmosdb update --enable-multiple-write-locations true.
- Conflict resolution: Last Write Wins (default, uses _ts; the NoSQL API also allows a custom numerical path) or Custom, which needs a registered merge stored procedure; unresolved conflicts go to the conflicts feed.
- Multi-region write accounts cannot be configured for strong consistency.
- Minimise conflicts in the application; the multi-region writes page lists antipatterns to avoid.

## Gotcha
Under Last Write Wins the item with the highest conflict resolution path value wins, and a delete always wins over an insert or replace; design counters and inventory carefully.

## Checked

2026-11-03. Confirmed against "Conflict types and resolution policies", the multi-region writes page and the az cosmosdb reference (--enable-multiple-write-locations exists on update): LWW default on _ts, custom numerical path for NoSQL, merge procedure, conflicts feed, no strong consistency, delete wins.
Removed: the route-each-user-to-one-region advice and "silently discards" wording (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Concurrent writes in two regions converge and the conflict feed is empty or handled.
