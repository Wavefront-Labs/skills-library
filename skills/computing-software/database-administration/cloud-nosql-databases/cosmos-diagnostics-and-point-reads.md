---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-diagnostics-and-point-reads
name: cosmos-diagnostics-and-point-reads
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-diagnostics-and-point-reads, cosmos-sdk-patterns, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Troubleshoot slow operations using diagnostics and favour point reads."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostics and point reads

**Goal:** Troubleshoot slow operations using diagnostics and favour point reads.

## Steps
- Log the Diagnostics property (present on every response, including CosmosException) when a request exceeds your expected latency; do not parse the string, its format changes between SDK versions.
- A point read (ReadItemAsync with id and partition key) of an item of about 1 KB costs 1 RU.
- Use continuation tokens to page query results.
- Scope queries to a partition key whenever the query allows it.

## Gotcha
Any query that filters on properties other than id without the partition key is a cross-partition query.

## Checked

2026-11-03. Confirmed against the .NET best-practices page (SDK logging, Diagnostics on all responses, retries and transient failures recorded) and the request units page (1 RU for a ~1 KB point read) and partitioning overview (cross-partition queries).
Removed: the 1000 ms threshold, MaxItemCount, QueryRequestOptions.PartitionKey and OFFSET LIMIT cost claims, and the RU fan-out growth claim (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Diagnostics for slow calls show any retries or transient failures, and the long-tail operations are explained.
