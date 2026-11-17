---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-session-tokens-and-staleness
name: cosmos-session-tokens-and-staleness
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-session-tokens-and-staleness, cosmos-consistency, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Handle session consistency across clients and regions."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels
  - https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-manage-consistency
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session tokens and staleness

**Goal:** Handle session consistency across clients and regions.

## Steps
- Each response returns a session token; the SDK tracks session tokens automatically, and tokens are partition-bound.
- To share across instances, get the token from the response, store it with the user session and set it per request; if you set none, the SDK uses its most recent token.
- Understand staleness with the Probabilistically Bounded Staleness (PBS) metric; for bounded staleness, az cosmosdb accepts --max-staleness-prefix of 10 to 2,147,483,647 and --max-interval of 5 to 86400 seconds.
- Keep one CosmosClient per application and reuse it so the token persists.

## Gotcha
Tokens are tracked per SDK client instance; another instance does not have your token unless you pass it, so its reads may be older than your last write.

## Checked

2026-11-03. Confirmed against "Manage consistency levels" (partition-bound tokens, automatic SDK tracking, manual get and set, PBS metric) and the az cosmosdb reference (--max-interval and --max-staleness-prefix ranges).
Removed: the SessionToken property name, the "Replication latency metrics" name and the multi-region minimum-bounds claim (not on the pages).
Method: documentation only; no commands were run.

## Verify
- [ ] Two client instances using the shared token read the item written by the other.
