---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-hierarchical-partition-keys
name: cosmos-hierarchical-partition-keys
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-hierarchical-partition-keys, cosmos-partitioning, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Use up to three key levels to avoid the 20 GB logical partition cap and target queries."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/partitioning-overview
  - https://learn.microsoft.com/en-us/azure/cosmos-db/hierarchical-partition-keys
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hierarchical partition keys

**Goal:** Use up to three key levels to avoid the 20 GB logical partition cap and target queries.

## Steps
- Define paths such as ["/tenantId","/userId","/sessionId"] when creating the container; only specific SDK versions support hierarchical keys (see the supported-versions table on the hierarchical partition keys page).
- Queries that supply a prefix of the key route to a subset of partitions rather than fan out.
- Choose levels from coarse to fine; the first level should still distribute well across tenants.
- Can replace synthetic keys that combine fields; with a synthetic key, tenant-level queries stay cross-partition.

## Gotcha
Hierarchical keys must be set at container creation and cannot be changed on an existing container; create a new container and move the data with a container copy job.

## Checked

2026-11-03. Confirmed against the hierarchical partition keys page and partitioning overview: up to three levels, 20 GB logical partition limit, prefix queries routed to a subset of physical partitions, high-cardinality first level, set at creation, migrate via container copy, SDK version table.
Removed: the "confirm SDK version support" hedge (replaced by a pointer to the page).
Method: documentation only; no commands were run.

## Verify
- [ ] A query on tenantId plus userId shows a low RU charge and no cross-partition fan-out in diagnostics.
