---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-time-to-live-configuration
name: cosmos-time-to-live-configuration
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-time-to-live-configuration, cosmos-ttl-and-lifecycle, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Expire data automatically."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/time-to-live
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-time-to-live
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time to live configuration

**Goal:** Expire data automatically.

## Steps
- Container DefaultTimeToLive: null or missing disables TTL, -1 enables it with no default expiry, a positive integer is seconds.
- Per-item ttl overrides defaultTtl; set -1 to retain an item.
- Expiry counts from the item's last modified time, so updates reset the clock.
- Expired items are removed in the background using spare RU/s.

## Gotcha
Item-level ttl applies only if the container's DefaultTimeToLive is present and not null; an item ttl must be -1 or a positive integer up to 2147483647 (null is not supported).

## Checked

2026-11-03. Confirmed against "Time to live in Azure Cosmos DB" and "Configure time to live": DefaultTimeToLive null, -1 and seconds, item override, last-modified basis, leftover RU deletion, expired items stop appearing in queries immediately, item ttl rules.
Removed: the _ts attribute name (not on the pages). Fixed the dead nosql/ source URL.
Method: documentation only; no commands were run.

## Verify
- [ ] An item with ttl 60 disappears from queries shortly after one minute.
