---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-account-and-container-limits
name: cosmos-account-and-container-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-account-and-container-limits, cosmos-limits, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Know the hard limits before designing."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/concepts-limits
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account and container limits

**Goal:** Know the hard limits before designing.

## Steps
- Item size 2 MB (UTF-8 length of the JSON); logical partition 20 GB; id up to 1,023 bytes; partition key value up to 2,048 bytes (101 bytes if large partition keys are not enabled).
- Container maximum throughput 1,000,000 RU/s by default (raise via an Azure support ticket); minimum 400 RU/s manual (or 1000 max RU/s for autoscale).
- Up to 500 databases and containers per account (this limit cannot be increased) and 25 containers on a shared-throughput database.
- Maximum response size (for example a paginated query) is 4 MB; a query that reaches the execution timeout or size limit returns a page and a continuation token.

## Gotcha
Limits change over time and some can be raised by support ticket; check the current limits page.

## Checked

2026-11-03. Confirmed against "Azure Cosmos DB service quotas" (concepts-limits): item size, partition key and id lengths, 20 GB logical partition, 1,000,000 RU/s with support-ticket increase, 400 and 1000 RU/s minimums, 25-container shared database, 500 databases and containers, 4 MB response.
Removed: "by SKU and region" (unsupported). Corrected id length from characters to bytes.
Method: documentation only; no commands were run.

## Verify
- [ ] The design values sit well below limits and are recorded as assumptions.
