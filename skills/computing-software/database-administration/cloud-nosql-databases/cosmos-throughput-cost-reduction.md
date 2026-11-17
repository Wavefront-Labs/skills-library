---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-throughput-cost-reduction
name: cosmos-throughput-cost-reduction
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-throughput-cost-reduction, cosmos-cost, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Reduce RU spend by tuning queries, indexes and provisioning."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/optimize-cost-throughput
  - https://learn.microsoft.com/en-us/azure/cosmos-db/free-tier
  - https://learn.microsoft.com/en-us/azure/cosmos-db/reserved-capacity
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-choose-offer
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throughput cost reduction

**Goal:** Reduce RU spend by tuning queries, indexes and provisioning.

## Steps
- Remove unused indexed paths (fewer indexed properties lower write RU), use point reads and use partition keys in queries.
- Use reserved capacity (one- or three-year commitment) for steady RU/s; free tier gives the first 1000 RU/s and 25 GB of storage on one account per subscription and is not available for serverless accounts.
- Right-size using Normalized RU Consumption, and use autoscale where average utilisation is below 66 percent.
- For dev/test, use free tier or the downloadable emulator.

## Gotcha
Throughput is made available in every region, so each added region adds cost; replicate only where needed.

## Checked

2026-11-03. Confirmed against the free tier page (1000 RU/s and 25 GB, one account per subscription, not for serverless), reserved capacity page (one-year or three-year commitment), choose-offer page (66 percent rule, Normalized RU Consumption) and optimize cost page (limit indexed properties, point reads, regions, dev/test options).
Removed: the discount figures (pricing), scale-down scripts, the project-only-needed-properties tip, and the serverless dev/test suggestion (not supported by the pages read).
Method: documentation only; no commands were run.

## Verify
- [ ] Monthly cost per request falls and average normalised RU utilisation is near the target.
