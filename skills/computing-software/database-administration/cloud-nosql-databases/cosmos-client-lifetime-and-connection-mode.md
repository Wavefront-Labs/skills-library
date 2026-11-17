---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-client-lifetime-and-connection-mode
name: cosmos-client-lifetime-and-connection-mode
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-client-lifetime-and-connection-mode, cosmos-sdk-patterns, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Reuse one SDK client and pick the right connection mode."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client lifetime and connection mode

**Goal:** Reuse one SDK client and pick the right connection mode.

## Steps
- Use a single CosmosClient instance for the lifetime of the application.
- Use direct mode for the best performance (gateway mode uses HTTP for both data and metadata); set ApplicationRegion or ApplicationPreferredRegions.
- Enable bulk support in the SDK for dumping large volumes of data when you do not need to optimise for latency.
- Use the latest SDK version; for end-to-end timeouts use both RequestTimeout and a CancellationToken.

## Gotcha
A client per request defeats the singleton guidance, and each new client fetches account metadata (consistency level, databases, containers, partitions) when it initialises.

## Checked

2026-11-03. Confirmed against "Performance and best practices for the .NET SDK" and the 429 troubleshooting page: singleton client, direct versus gateway, ApplicationRegion/ApplicationPreferredRegions, bulk support, latest SDK, RequestTimeout plus CancellationToken, metadata fetch at initialisation.
Removed: TCP wording, the AllowBulkExecution property name, and the socket-exhaustion claim (not supported by those pages); description reworded to match.
Method: documentation only; no commands were run.

## Verify
- [ ] One client instance is reused (check DI registration) and P99 latency is stable.
