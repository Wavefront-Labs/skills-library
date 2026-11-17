---
id: computing-software.search-and-information-retrieval.typesense.compact-database-and-clear-cache
name: compact-database-and-clear-cache
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [db-compaction, rocksdb, clear-cache, typesense]
level: practitioner
status: docs-checked
description: "Compact Typesense's RocksDB store with POST /operations/db/compact to cut size and read latency, and flush the use_cache LRU with /operations/cache/clear."
sources: ["https://typesense.org/docs/30.2/api/cluster-operations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compaction and cache clearing

## Compact the on-disk database

Documents are stored in RocksDB. After frequent writes or updates, compaction can reduce database size and read latency. The database does not block during it, but run it at off-peak hours.

`curl -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" -X POST http://localhost:8108/operations/db/compact`

For the automatic compaction interval and cache size flags, see the server configuration page of the Typesense docs.

## Clear the search cache

Search responses sent with the `use_cache` parameter are stored in an LRU cache. Clear it completely with:

`curl -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" -X POST http://localhost:8108/operations/cache/clear`

## Checked

Method: 2026-11-09 docs-only read of the cited Cluster Operations page in full. Confirmed the compaction paragraph, both endpoints and the use_cache LRU cache. Removed the default interval and cache-entry figures, which are on a server configuration page not read here.
