---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-query-limits
name: cosmos-query-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-query-limits, cosmos-limits, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Write queries that stay efficient."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/join
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/pagination
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query limits and patterns

**Goal:** Write queries that stay efficient.

## Steps
- Avoid cross-partition queries for hot paths; supply the partition key.
- Page with continuation tokens; a query that hits the execution timeout or 4 MB response size returns a page plus a continuation token.
- JOINs work only within a single item; they cannot join across items or containers.
- Enable SQL query metrics in the .NET SDK for more detail on backend query execution.

## Gotcha
If you need to join across items or containers, rework the data model rather than the query.

## Checked

2026-11-03. Confirmed against service quotas (4 MB response, timeout returns continuation token), the JOIN page (single item only) and the pagination page (continuation tokens), and the .NET best-practices page (SQL query metrics).
Removed: the OFFSET cost claim, the PopulateQueryMetrics property name and the retrieved-versus-output document count heuristic (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Hot-path queries supply the partition key and their RequestCharge is recorded and acceptable.
