---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-retry-and-backoff
name: cosmos-retry-and-backoff
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-retry-and-backoff, cosmos-throttling, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Configure the SDK to absorb transient throttling."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/troubleshoot-request-rate-too-large
  - https://learn.microsoft.com/en-us/azure/cosmos-db/conceptual-resilient-sdk-applications
  - https://learn.microsoft.com/en-us/azure/cosmos-db/performance-tips-dotnet-sdk-v3
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry policy and backoff

**Goal:** Configure the SDK to absorb transient throttling.

## Steps
- SDKs retry 429s automatically (typically up to nine times) and honour the x-ms-retry-after-ms header; in the .NET SDK v3 a 429 surfaces as a CosmosException after a cumulative wait of 30 seconds by default, even when the retry count is below the maximum.
- The retry count and wait time are options on CosmosClientOptions; use lower values for latency-sensitive requests and handle CosmosException with StatusCode 429 at the application level (a 429 is safe to retry).
- Add exponential backoff in application code, and for metadata operations send requests at a lower rate.
- Set autoscale max RU/s with headroom: autoscale scales to the maximum only when normalised RU consumption stays at 100 percent for a sustained period.

## Gotcha
Layering your own retries on top of the SDK's prolongs throttling; use exponential backoff and cap them.

## Checked

2026-11-03. Confirmed against the 429 troubleshooting page (automatic retries, typically nine, exponential backoff advice, metadata backoff), "Designing resilient applications" (x-ms-retry-after-ms, 429 safe to retry), the .NET performance tips page (30 s cumulative wait, default of 9, CosmosClientOptions) and the provisioned autoscale page.
Removed: the MaxRetryAttemptsOnRateLimitedRequests and MaxRetryWaitTimeOnRateLimitedRequests property names (not on the pages), the client-side bulk throttling and jitter advice. Fixed the dead nosql/ source URL.
Method: documentation only; no commands were run.

## Verify
- [ ] Under a load test the application sees few surfaced 429s and latency stays inside the objective.
