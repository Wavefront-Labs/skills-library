---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-change-feed-processor
name: cosmos-change-feed-processor
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-change-feed-processor, cosmos-change-feed, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Consume changes with scalable, checkpointed workers."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-processor
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change feed processor

**Goal:** Consume changes with scalable, checkpointed workers.

## Steps
- The change feed returns inserts and updates in order per partition key (latest version mode); deletes are not included in that mode, so use soft deletes with a TTL.
- Change feed processor in the SDK: GetChangeFeedProcessorBuilder with a lease container; multiple hosts share leases for scale.
- Alternatively host the processor in a serverless function in Azure Functions.
- All versions and deletes mode provides deletes, TTL expirations and intermediate versions; it requires continuous backup on the account.

## Gotcha
A lease is owned by one instance at a time, so run no more instances than there are leases.

## Checked

2026-11-03. Confirmed against the change feed processor, change feed overview and change feed modes pages: per-partition-key ordering, deletes absent in latest-version mode, GetChangeFeedProcessorBuilder, lease container shared across instances, at-least-once delivery, Azure Functions as a host, continuous-backup requirement for all versions and deletes mode.
Removed: the lease container /id partition key rule and lease RU sizing advice (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Starting a second host redistributes leases and each change is processed at least once.
