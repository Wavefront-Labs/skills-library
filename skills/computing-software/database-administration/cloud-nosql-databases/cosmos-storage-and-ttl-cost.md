---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-storage-and-ttl-cost
name: cosmos-storage-and-ttl-cost
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-storage-and-ttl-cost, cosmos-cost, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Control storage cost by expiring data and offloading analytics."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/optimize-cost-throughput
  - https://learn.microsoft.com/en-us/azure/cosmos-db/time-to-live
  - https://learn.microsoft.com/en-us/azure/cosmos-db/analytical-store-introduction
  - https://learn.microsoft.com/en-us/azure/cosmos-db/continuous-backup-restore-introduction
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage, TTL and analytical store

**Goal:** Control storage cost by expiring data and offloading analytics.

## Steps
- Container TTL: set DefaultTimeToLive in seconds (-1 means on with no default expiry; null or missing means off); a per-item ttl overrides it; deletion of expired items uses leftover RUs.
- Analytical store is a fully isolated column store: analytical queries do not affect transactional workloads and need no separate RUs. Azure Synapse Link is no longer supported for new projects.
- Keep items small: the request charge of an operation correlates with item size.
- Continuous backup: the 30-day and 35-day tiers add a monthly charge for backup storage, the 7-day tier does not, and every tier charges when you restore.

## Gotcha
TTL deletes use leftover RU/s, so expiry lags under heavy load.

## Checked

2026-11-03. Confirmed against the time to live, analytical store, continuous backup and optimize cost pages: DefaultTimeToLive semantics, leftover-RU deletion, isolated column store without separate RUs, Synapse Link not supported for new projects, item size and cost, continuous backup tier charges.
Removed: the Blob Storage advice and the billing hedge (replaced by documented facts); the page-specific price rates are not repeated.
Method: documentation only; no commands were run.

## Verify
- [ ] Storage growth is flat after TTL and the analytical queries do not appear in transactional RU.
