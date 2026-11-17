---
id: computing-software.database-administration.neo4j.capacity-planning
name: capacity-planning
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, store-size-estimate, ram-for-pagecache, core-count, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Sizing"
sources: ["https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/", "https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-memrec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity planning

Goal: size servers.
- The memory configuration page gives worked methods to estimate page cache for an existing database and for a planned one; follow them rather than a rule of thumb.
- Use `neo4j-admin server memory-recommendation --memory=<size>` to see the heap and page cache split for a given amount of RAM.
- Leave RAM outside heap and page cache for the OS, Lucene indexes and any vector index (held in OS memory).
- With CDC enabled, more data is written to transaction logs, which rotate and prune more often; make sure the log disk has room.
Verify: the estimate matches the memory settings in `neo4j.conf`.

## Checked

2026-11-02. Confirmed in the memory configuration page, memory-recommendation page and the CDC self-managed page. Removed: the cores-versus-latency claim and generic disk advice (not documented).
Method: documentation only; no commands were run.
