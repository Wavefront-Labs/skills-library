---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-partition-key-selection
name: cosmos-partition-key-selection
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-partition-key-selection, cosmos-partitioning, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Pick a partition key with high cardinality that appears in most queries and spreads storage and RU evenly."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview
  - https://learn.microsoft.com/en-us/azure/cosmos-db/hierarchical-partition-keys
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb/sql/container
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partition key selection

**Goal:** Pick a partition key with high cardinality that appears in most queries and spreads storage and RU evenly.

## Steps
- A logical partition is limited to 20 GB and 10,000 RU/s; each physical partition provides up to 10,000 RU/s and is split by the service when it exceeds 50 GB.
- Choose a high-cardinality property that matches your query filters (for example tenantId, userId or deviceId); a low-cardinality field such as status suits only small data volumes.
- Filter every hot query on the partition key to avoid cross-partition fan-out.
- Create the container with the path, for example az cosmosdb sql container create -a ACCOUNT -g RG -d db -n orders -p /customerId --throughput 400
- The key path cannot be changed after creation, and an item's partition key value is immutable.

## Gotcha
A hot logical partition throttles at the per-partition RU share even when the container has spare RU/s overall.

## Checked

2026-11-03. Confirmed against the partitioning overview and hierarchical partition keys pages (20 GB and 10,000 RU/s logical limits, 50 GB physical split, high cardinality, immutable values, cross-partition queries) and the az cosmosdb sql container create reference (-a, -g, -d, -n, -p/--partition-key-path, --throughput all exist).
Removed: the "confirm current limits" hedge and the date-alone example (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Normalised RU consumption is balanced across PartitionKeyRangeIds and no logical partition is near 20 GB.
