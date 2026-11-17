---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-429-diagnosis
name: cosmos-429-diagnosis
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-429-diagnosis, cosmos-throttling, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Find why requests return HTTP 429 and fix the cause."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/troubleshoot-request-rate-too-large
  - https://learn.microsoft.com/en-us/azure/cosmos-db/conceptual-resilient-sdk-applications
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing 429 errors

**Goal:** Find why requests return HTTP 429 and fix the cause.

## Steps
- Check Metrics: the count of 429 responses and Normalized RU Consumption per PartitionKeyRangeId.
- If one PartitionKeyRangeId is consistently at 100 percent while others sit at about 30 percent or less, that signals a hot partition; if all are high, the provisioned RU/s are likely too low.
- Check whether the 429 is on data operations or metadata (database/container) requests.
- Look at the x-ms-retry-after-ms header for suggested backoff.

## Gotcha
Raising total RU/s will not fix a single hot logical partition; change the key or spread the writes.

## Checked

2026-11-03. Confirmed against the Cosmos DB pages "Diagnose and troubleshoot Request rate too large (429)" and "Designing resilient applications": hot-partition signature on Normalized RU Consumption per PartitionKeyRangeId, data versus metadata 429s, x-ms-retry-after-ms. Removed: the 1 to 5 percent target (unsupported). Fixed the dead nosql/ source URL.
Method: documentation only; no commands were run.

## Verify
- [ ] Normalised RU consumption no longer sits at 100 percent for sustained periods and 429s stop reaching the application.
