---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-transactions-and-stored-procedures
name: cosmos-transactions-and-stored-procedures
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-transactions-and-stored-procedures, cosmos-data-modelling, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Get atomic multi-item changes within a logical partition."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/stored-procedures-triggers-udfs
  - https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits
  - https://learn.microsoft.com/en-us/azure/cosmos-db/conceptual-resilient-sdk-applications
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transactions and server-side programming

**Goal:** Get atomic multi-item changes within a logical partition.

## Steps
- A transactional batch supports up to 100 operations on items with the same partition key.
- Stored procedures, triggers and UDFs are written in JavaScript; operations within one stored procedure or trigger are atomic (all succeed or none), and you must supply a partition key value when running one.
- Optimistic concurrency: send the item's ETag as a precondition; a mismatch returns 412 (retry after reading the latest version).
- Atomic multi-item operations are scoped to a single partition key value.

## Gotcha
Batch operations spanning partition keys fail; group the data by the same key.

## Checked

2026-11-03. Confirmed against service quotas (100 operations in a transactional batch, same partition key), "Stored procedures, triggers, and UDFs" and its how-to (JavaScript, atomic within one procedure, partition key required) and "Designing resilient applications" (412 precondition failure on ETag mismatch).
Removed: the stored procedure time limit, the TransactionalBatch and IfMatchEtag names, and the explicit cross-partition wording (not on the pages). Replaced the unrelated modelling source.
Method: documentation only; no commands were run.

## Verify
- [ ] A failing operation in the batch rolls back all and an ETag conflict returns 412.
