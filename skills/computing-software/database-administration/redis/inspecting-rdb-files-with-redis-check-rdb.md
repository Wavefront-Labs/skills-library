---
id: computing-software.database-administration.redis.inspecting-rdb-files-with-redis-check-rdb
name: inspecting-rdb-files-with-redis-check-rdb
category: computing-software
field: database-administration
product: redis
tags: [database-administration, redis, redis-check-rdb, rdb, redis-persistence, rdb-analysis, backup-verification]
level: practitioner
status: docs-checked
description: "Verify Redis RDB snapshot integrity with redis-check-rdb, inspect contents and memory by key with rdb-tools style analysers, and test-restore before trusting a backup."
sources:
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://github.com/redis/redis/blob/unstable/src/redis-check-rdb.c
  - https://github.com/sripathikrishnan/redis-rdb-tools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting RDB files (redis-check-rdb)

**Goal:** prove a snapshot is readable before it becomes your only copy, and find what consumes memory without touching production.

## Integrity check
```bash
redis-check-rdb /var/lib/redis/dump.rdb
```
Output ends with `\o/ RDB looks OK! \o/` on success; on corruption it reports the offset and the last key read. It ships with Redis (the check runs when the server binary is invoked under the `redis-check-rdb` name). Run it in the backup pipeline after every copy.

## Info inside the file
The checker prints each AUX field stored in the file as `AUX FIELD name = 'value'`. `redis-check-aof` is the AOF equivalent (multipart AOF in 7.0+: point it at the manifest).

## Memory analysis offline
- `rdb -c memory dump.rdb -f mem.csv` (redis-rdb-tools, Python) writes a CSV of approximate memory per key. Check the tool's own docs for which RDB versions it supports; other third-party analysers exist.
- Sort by size to find big keys and prefixes; compare with `redis-cli --bigkeys` / `--memkeys` sampling on a live replica.

## Test restore
```bash
mkdir -p /tmp/rdbtest && cp dump.rdb /tmp/rdbtest/
redis-server --port 6390 --dir /tmp/rdbtest --dbfilename dump.rdb --save '' --appendonly no &
redis-cli -p 6390 DBSIZE
redis-cli -p 6390 INFO keyspace
```
Compare DBSIZE with the source's at snapshot time (from `INFO keyspace` logged by the backup job).

## Gotchas
- A file truncated during copy fails the check: copy after `BGSAVE` completes (`rdb_bgsave_in_progress:0`, `rdb_last_bgsave_status:ok` in `INFO persistence`), and copy to a temp name then rename.
- Modules' data types (JSON, Bloom) need the module loaded to restore (built into Redis 8).

## Verify
Backup job exits non-zero if `redis-check-rdb` does not print the OK line, and a weekly test restore records the key count.

## Checked
Date: 2026-10-23. Documentation release: Redis documentation at redis.io/docs/latest and the redis/docs and redis/redis 8.2 repositories as read on 2026-10-23.
Confirmed from redis-check-rdb.c: usage `redis-check-rdb <rdb-file-name>`, success line, errors report `[offset N]` and the key being read, AUX fields printed as `AUX FIELD`; runs under the redis-check-rdb alias of the server binary. Confirmed from redis-check-aof.c: the argument can be a `.manifest` (multi-part AOF) or an AOF file. Confirmed redis-rdb-tools command `rdb -c memory ... -f memory.csv`. Confirmed from the persistence page that the RDB is written under a temporary name and renamed atomically, and that Redis 8 bundles previously modular data types. Removed unconfirmed: per-DB key count output, claims about successor tools.
Method: documentation only; no commands were run.
