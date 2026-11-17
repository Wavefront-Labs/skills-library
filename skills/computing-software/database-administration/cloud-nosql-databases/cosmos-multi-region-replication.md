---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-multi-region-replication
name: cosmos-multi-region-replication
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-multi-region-replication, cosmos-global-distribution, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Add read regions and plan failover."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/distribute-data-globally
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb
  - https://learn.microsoft.com/en-us/azure/reliability/reliability-cosmos
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-region replication and failover

**Goal:** Add read regions and plan failover.

## Steps
- az cosmosdb update --locations regionName=westeurope failoverPriority=1 isZoneRedundant=false (repeat --locations once per region; failover priority 0 is the write region, higher values are read regions, and each value must be unique).
- Enable automatic failover (--enable-automatic-failover), change priorities with az cosmosdb failover-priority-change, and rehearse a failover in a drill.
- Set ApplicationPreferredRegions (or ApplicationRegion) in the v3 SDK; reads go to the first region in the list during failovers.
- Zone redundancy is configured per region and gives higher availability SLAs than accounts without zones.

## Gotcha
Throughput you provision is made available in every region, so each added region adds cost; replicate only where needed.

## Checked

2026-11-03. Confirmed against the az cosmosdb reference (update --locations with regionName, failoverPriority and isZoneRedundant keys, --enable-automatic-failover, failover-priority-change), the .NET best-practices page (ApplicationPreferredRegions), and the Cosmos DB reliability page (zone redundancy per region, higher SLA).
Removed: "RU billing equal to provisioned RU/s" wording (replaced by the documented behaviour).
Method: documentation only; no commands were run.

## Verify
- [ ] Manual failover drill completes with the app reconnecting and the expected region serving writes.
