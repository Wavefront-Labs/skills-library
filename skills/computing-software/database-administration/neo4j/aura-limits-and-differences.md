---
id: computing-software.database-administration.neo4j.aura-limits-and-differences
name: aura-limits-and-differences
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, aura, auradb, aura-api, apoc, multi-database, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Know what AuraDB does not offer compared with self-managed Neo4j: multi-database, full APOC, TLS ciphers, and the Aura API for automation."
sources: ["https://neo4j.com/docs/aura/auradb/", "https://neo4j.com/docs/aura/platform/api/overview/", "https://neo4j.com/docs/aura/platform/apoc/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aura vs self-managed differences

Goal: know the constraints before moving a workload to AuraDB.
- Multi-database is not currently supported within AuraDB.
- Only a subset of APOC Core functions and procedures is pre-installed. Check the Aura APOC support page for the list before relying on one.
- AuraDB accepts only a restricted list of TLS cipher suites during the handshake.
- Automate through the Aura API (base URL `https://api.neo4j.io`, version v1, for example `GET https://api.neo4j.io/v1/instances`) after creating API credentials. Rate limiting is 125 requests per minute. Retry only idempotent requests, with backoff, because retrying an instance create can produce duplicate billed instances.
- To move data in, the migration guide uses a dump and `neo4j-admin database upload`, or you import a snapshot dump through the console.
Verify: automation uses the Aura API with backoff, and no code depends on a second database or an APOC procedure that is not in the Aura subset.

## Checked

2026-11-09. Confirmed against the neo4j/docs-aura sources (auradb create-database note on multi-database, platform/apoc and its procedure partial, platform/security/secure-connections cipher-suite note, platform/api/overview, tutorials/migration and tutorials/upgrade). Removed: "no filesystem access" and "some config and plugins are restricted" (not stated on those pages), the "confirm list" placeholder, and the italic draft disclaimer.

Method: documentation only; no commands were run.
