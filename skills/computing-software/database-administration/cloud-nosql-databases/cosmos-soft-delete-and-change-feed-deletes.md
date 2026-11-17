---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-soft-delete-and-change-feed-deletes
name: cosmos-soft-delete-and-change-feed-deletes
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-soft-delete-and-change-feed-deletes, cosmos-ttl-and-lifecycle, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Capture deletions for downstream consumers."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/time-to-live
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-modes
  - https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft delete and deletes in the change feed

**Goal:** Capture deletions for downstream consumers.

## Steps
- In latest-version mode deletes do not appear; mark items with a deleted flag and a short ttl so consumers see the update before the TTL removes it.
- All versions and deletes mode (needs continuous backup) exposes deletes and TTL expirations directly.
- Filter application queries so items flagged as deleted are excluded.
- Set the marker item's TTL longer than the slowest consumer lag.

## Gotcha
TTL expiry produces no change feed entry in latest-version mode.

## Checked

2026-11-03. Confirmed against the change feed modes page (latest version mode does not log deletes; soft-delete flag such as deleted = true plus TTL; all versions and deletes mode needs continuous backup) and the change feed overview (deletes and TTL expirations captured only in all versions and deletes mode).
Removed: the IS_DEFINED query form (not on the pages). Fixed the dead nosql/ time-to-live source URL.
Method: documentation only; no commands were run.

## Verify
- [ ] Consumers see the delete marker before the item is physically removed.
