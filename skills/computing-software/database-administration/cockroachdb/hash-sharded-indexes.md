---
id: computing-software.database-administration.cockroachdb.hash-sharded-indexes
name: hash-sharded-indexes
category: computing-software
field: database-administration
product: cockroachdb
tags: [hash-sharded-indexes, sequential-keys, hotspots, bucket-count, shard-columns]
level: practitioner
status: docs-checked
description: "Remove sequential-key write hotspots in CockroachDB with hash-sharded indexes: USING HASH, bucket_count, shard_columns, partitioned-table limits and read trade-offs."
sources:
  - https://www.cockroachlabs.com/docs/stable/hash-sharded-indexes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread writes for monotonically increasing keys (timestamps, sequential IDs) across ranges and nodes.

How it works: the index includes a hidden virtual computed shard column; CockroachDB uses it to distribute values across buckets, avoiding a single hot range. Cost: range scans over sequential data get slower because they must read every bucket and merge results. It is hash partitioning, not hash indexing.

Create by adding `USING HASH` to `CREATE INDEX`, `CREATE TABLE`, or `ALTER PRIMARY KEY`:
```sql
CREATE INDEX idx_region_city ON data_test (region, city, population)
  USING HASH WITH (bucket_count = 4, shard_columns = (region));
```
- Bucket count defaults from the cluster setting `sql.defaults.default_hash_sharded_index_bucket_count`; specify `bucket_count` per index to override. More buckets give more write throughput but make scans more expensive. Test your workload with different counts if the default does not fit.
- `shard_columns` hashes only a prefix of the key columns (it must match a prefix of the index columns). Use it when queries constrain the leading columns but still scan or sort by later ones within a shard. Default is hashing all key columns.

Restrictions:
- A hash-sharded index can be implicitly partitioned (`REGIONAL BY ROW` or `PARTITION ALL BY`, the latter in preview) only if the partition column, such as `crdb_region`, is not among its columns.
- Indexes explicitly partitioned with `PARTITION BY` cannot be hash-sharded.

Version note: indexes created in v22.1 and later do not backfill the shard column because it is virtual. Indexes created in v21.2 or earlier use a physical `STORED` shard column, which still exists.

Verify: `SHOW CREATE TABLE <table>;` shows the index with `USING HASH` and its `bucket_count`.

## Checked
2026-11-03. Confirmed on the hash-sharded indexes page: hash partitioning not hash indexing, `bucket_count` and `shard_columns` (must match an index column prefix), `sql.defaults.default_hash_sharded_index_bucket_count`, bucket count trade-off, the REGIONAL BY ROW and PARTITION ALL BY (preview) restrictions, explicit `PARTITION BY` exclusion, v22.1 virtual shard column versus v21.2 `STORED`. Removed: the hidden column name pattern and the latency claim.
Method: documentation only; no commands were run.
