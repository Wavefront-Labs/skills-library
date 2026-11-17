---
id: computing-software.database-administration.neo4j.memory-sizing
name: memory-sizing
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, page-cache-size, heap-initial-size, neo4j-admin-memrec, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Memory configuration"
sources: ["https://neo4j.com/docs/operations-manual/current/performance/memory-configuration/", "https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin/neo4j-admin-memrec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap and page cache sizing

Goal: size memory.
- `neo4j-admin server memory-recommendation [--memory=<size>]` prints heuristic heap and page cache settings that can be pasted into `neo4j.conf`. It assumes the machine is dedicated to Neo4j; otherwise pass `--memory` (units k, K, m, M, g, G).
- Heap is set by `server.memory.heap.initial_size` and `server.memory.heap.max_size`; the docs recommend the same value for both to avoid unwanted full garbage collection pauses.
- The page cache (`server.memory.pagecache.size`) caches graph data and indexes from disk; a vector index is loaded in OS memory, not the page cache.
- Define page cache and heap explicitly in `neo4j.conf`; otherwise Neo4j computes heuristic values at startup.
- If a query is terminated by the transaction memory limit, the docs suggest re-running it with the limit disabled to see whether heap use is acceptable.
Verify: `neo4j.conf` has explicit heap and page cache values and the server starts with them.

## Checked

2026-11-02. Confirmed in the memory configuration page and the memory-recommendation page. Removed: the 98% hit-ratio target (not documented).
Method: documentation only; no commands were run.
