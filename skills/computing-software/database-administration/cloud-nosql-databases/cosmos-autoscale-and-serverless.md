---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-autoscale-and-serverless
name: cosmos-autoscale-and-serverless
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-autoscale-and-serverless, cosmos-throughput, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Choose the throughput model for the workload."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/provision-throughput-autoscale
  - https://learn.microsoft.com/en-us/azure/cosmos-db/serverless
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-choose-offer
  - https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autoscale, manual and serverless throughput

**Goal:** Choose the throughput model for the workload.

## Steps
- Manual: fixed RU/s billed hourly; Autoscale: set max RU/s (Tmax), throughput scales between 10 percent and 100 percent of Tmax and each hour is billed at the highest RU/s reached; Serverless: pay only for the RUs consumed plus storage, and the account can run in a single Azure region only.
- Shared throughput at database level (manual minimum 400 RU/s for the first 25 containers; autoscale minimum max 1000 RU/s for the first 25) versus dedicated per container.
- Change with az cosmosdb sql container throughput update, or switch between manual and autoscale with az cosmosdb sql container throughput migrate.
- Autoscale suits variable or hard-to-predict load; see the pricing page for rates.

## Gotcha
Microsoft's guidance: if you use the full provisioned RU/s for 66 percent of hours in a month or more, manual is estimated to cost less; if average normalised utilisation is below 66 percent, autoscale is estimated to save.

## Checked

2026-11-03. Confirmed against the Cosmos DB pages on autoscale throughput, serverless, choosing between manual and autoscale, service quotas, and the az cosmosdb sql container reference (throughput update and migrate exist): 0.1*Tmax to Tmax, hourly highest billing, single-region serverless, 400/1000 RU/s minimums for the first 25 containers, 66 percent rule.
Removed: the 1.5x price multiplier (pricing, not checkable) and the serverless storage-limit claim (unsupported).
Method: documentation only; no commands were run.

## Verify
- [ ] Normalised RU Consumption chart shows headroom without sustained 100 percent and cost matches the plan.
