---
id: computing-software.search-and-information-retrieval.meilisearch.compact-an-index
name: compact-an-index
category: computing-software
field: search-and-information-retrieval
product: meilisearch
tags: [index-compaction, fragmentation, index-size, meilisearch]
level: advanced
status: docs-checked
description: "Reclaim Meilisearch disk space with POST /indexes/<uid>/compact: when to run it, indexSize vs usedIndexSize, disk needs, search availability."
sources:
  - https://www.meilisearch.com/docs/capabilities/indexing/how_to/compact_an_index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compact an index

Adds, updates, deletes and settings changes leave unused space in an index. Compaction reorganizes it. It is never automatic; call `POST /indexes/<index_uid>/compact`, which returns a task of type `indexCompaction`. It passes through the queue and delays tasks queued behind it (indexing, settings), though search stays available.

## When

After bulk deletions, many updates, or unexpectedly high disk use. Not after every operation.

## Measure fragmentation

`GET /indexes/<uid>/stats` gives `indexSize` (database size on disk) and `usedIndexSize` (pages actually holding data). If the gap is more than about 30%, compaction may help. A baseline for indices updated a few times per day is a weekly check; scale cadence with write volume. `GET /stats` reports the same per index plus instance-wide `databaseSize` and `usedDatabaseSize`.

## Requirements

- Temporary free disk of roughly the index size; if the disk fills, the task fails and the index stays as before.
- Duration depends on fragmentation, not just size; compacting again soon after is much faster (close to copying the file). Schedule it in low-traffic hours.

## Checked

Method: 2026-11-09 docs-only read of the cited page in full. All claims match the page; unchanged except the shortened description.
