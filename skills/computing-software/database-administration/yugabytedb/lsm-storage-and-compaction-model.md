---
id: computing-software.database-administration.yugabytedb.lsm-storage-and-compaction-model
name: lsm-storage-and-compaction-model
category: computing-software
field: database-administration
product: yugabytedb
tags: [lsm, rocksdb, memtable, sst, compaction, bloom-filter, docdb, tombstones]
level: practitioner
status: docs-checked
description: "How DocDB stores data in an LSM tree with memtables and a single level of SST files, how deletes and compactions behave, and which counters expose read cost."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/architecture/docdb/lsm-sst.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/launch-and-manage/monitor-and-alert/metrics/cache-storage.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LSM storage and compaction model

DocDB is built on RocksDB, an LSM tree. Raft logs play the role of the write-ahead log, so there is no separate LSM WAL.

Write path: every insert, update and delete goes into an in-memory **memtable** (a sorted map). When it fills it becomes immutable and is flushed to disk as an **SST** file. DocDB keeps one active memtable and at most one immutable one at a time. SST files hold compressed data blocks, an index and a **bloom filter** used to skip files that cannot contain a key. The tserver runs several compaction queues and throttles compactions to avoid compaction storms.

Read path: check the memtable first, then SSTs, using index and bloom filter blocks to avoid disk reads. The primitive iterator operations are seek, next and previous; scans are a seek followed by many nexts.

Deletes write a **tombstone** marker. Space is only reclaimed when compaction drops the tombstone together with the data it covers.

Metrics to check read amplification and cache health: `rocksdb_number_db_seek`, `rocksdb_number_db_next`, `rocksdb_number_db_prev`, `rocksdb_block_cache_hit`, `rocksdb_block_cache_miss`, `bloom_filter_checked` and `bloom_filter_useful`. SST volume is in `current_version_sst_files_size`, `ts_active_data_size` and `ts_data_size`. `--db_block_cache_size_percentage` sizes the block cache.

## Checked

2026-11-04. Confirmed against the LSM and SST architecture page: RocksDB-based LSM, Raft log in place of the WAL, memtable and at most one immutable memtable, SST contents and bloom filter, read path, seek/next/prev, tombstones removed at compaction, compaction queues with throttling. Removed the single-level/size-tiered claim, the disk-use inference and the block cache default, which the page does not state.

Method: documentation only; no commands were run.
