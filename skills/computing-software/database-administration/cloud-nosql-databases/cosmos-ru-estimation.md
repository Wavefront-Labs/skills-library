---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-ru-estimation
name: cosmos-ru-estimation
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-ru-estimation, cosmos-throughput, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Estimate and measure the RU cost of operations before provisioning."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/request-units
  - https://learn.microsoft.com/en-us/azure/cosmos-db/optimize-cost-throughput
  - https://learn.microsoft.com/en-us/azure/cosmos-db/performance-tips-dotnet-sdk-v3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Request unit estimation

**Goal:** Estimate and measure the RU cost of operations before provisioning.

## Steps
- A point read (id plus partition key) of an item of about 1 KB costs 1 RU; write and query costs depend on item size, indexed properties and query shape.
- Read x-ms-request-charge from each response (RequestCharge in the SDK) and log it for the top operations.
- Use the capacity planner for an initial rough estimate, then refine with measured request charges.
- Prefer point reads (ReadItem with id and partition key) over queries by id.

## Gotcha
RU cost grows with indexed property count and item size; the same write on a heavily indexed item costs more.

## Checked

2026-11-03. Confirmed against the request units page (1 RU for a ~1 KB point read, item size and indexed properties affect RU), the .NET performance tips page (x-ms-request-charge header, RequestCharge property) and the optimize cost page (capacity planner for a rough initial estimate).
Removed: the ~5 RU per 1 KB write figure and the cross-partition and index-miss cost claims (not on the pages); the capacity-planner input list.
Method: documentation only; no commands were run.

## Verify
- [ ] Logged RequestCharge for the top 5 operations is totalled and fits within the provisioned RU/s with headroom.
