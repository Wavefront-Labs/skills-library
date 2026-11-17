---
id: computing-software.search-and-information-retrieval.typesense.server-resource-and-search-limits
name: server-resource-and-search-limits
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [resource-limits, filter-by-max-ops, thread-pool-size, typesense]
level: advanced
status: docs-checked
description: "Tune Typesense resource and search limits: thread pool, caches, write rejection, replication lag, snapshot and compaction intervals, page limits."
sources: ["https://typesense.org/docs/30.2/api/server-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource usage and search limits

## Resource parameters

| Parameter | Default and effect |
|---|---|
| `--thread-pool-size` | `NUM_CORES * 8`, threads for concurrent requests |
| `--num-collections-parallel-load` | `NUM_CORES * 4`, collections loaded in parallel at startup |
| `--num-documents-parallel-load` | `1000`, documents per collection indexed in parallel at startup |
| `--cache-num-entries` | `1000`, LRU cache of search responses |
| `--embedding-cache-num-entries` | `100`, LRU cache of text embeddings from remote embedders |
| `--disk-used-max-percentage` | `100`, writes rejected above this disk use (100 never rejects) |
| `--memory-used-max-percentage` | `100`, writes rejected above this memory use |
| `--healthy-read-lag` | `1000`, reads rejected when updates lag more |
| `--healthy-write-lag` | `500`, writes rejected when updates lag more |
| `--snapshot-interval-seconds` | `3600`, replication log snapshot frequency |
| `--db-compaction-interval` | `604,800` (7 days) |

Snapshotting often speeds recovery from a cold start, but on a large dataset too low a value can slow follower recovery. If you drop and recreate collections frequently, consider a compaction interval around 24 hours. `--skip-writes` starts the server without reading writes from the Raft log, to skip over recent bad writes after a crash.

## Search limits

`--filter-by-max-ops` (default `100` operators in `filter_by`), `--max-per-page` (`250`), `--max-group-limit` (`99`, the largest `group_limit`).

## RocksDB tuning

Documents live in RocksDB. `--db-write-buffer-size` (default 4MB), `--db-max-write-buffer-number` (`2`), `--db-max-log-file-size` (4MB), `--db-keep-log-file-num` (`5`) and `--max-indexing-concurrency` (`4`) can improve write performance in some cases.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Server Configuration (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
