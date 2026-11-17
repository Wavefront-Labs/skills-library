---
id: computing-software.database-administration.postgresql.pg-buffercache-and-pg-prewarm
name: pg-buffercache-and-pg-prewarm
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-buffercache, pg-prewarm, shared-buffers, cache-warming, autoprewarm, memory]
level: practitioner
status: verified
description: "Inspect what is in PostgreSQL shared_buffers with pg_buffercache and warm the cache after restart or failover with pg_prewarm and autoprewarm."
sources:
  - https://www.postgresql.org/docs/current/pgbuffercache.html
  - https://www.postgresql.org/docs/current/pgprewarm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspecting and warming the buffer cache

## What is cached (pg_buffercache)
```sql
CREATE EXTENSION pg_buffercache;
SELECT c.relname, count(*) AS buffers, pg_size_pretty(count(*) * 8192) AS cached,
       round(100.0 * count(*) / (SELECT setting::int FROM pg_settings WHERE name = 'shared_buffers'), 1) AS pct_of_cache,
       round(100.0 * count(*) * 8192 / nullif(pg_relation_size(c.oid),0), 1) AS pct_of_rel,
       sum(b.usagecount) / count(*) AS avg_usage, count(*) FILTER (WHERE b.isdirty) AS dirty
FROM pg_buffercache b JOIN pg_class c ON b.relfilenode = pg_relation_filenode(c.oid)
WHERE b.reldatabase = (SELECT oid FROM pg_database WHERE datname = current_database())
GROUP BY c.oid, c.relname ORDER BY buffers DESC LIMIT 20;
```
- Scanning the view takes buffer header locks briefly; avoid running it every few seconds on huge caches. `pg_buffercache_summary()` / `pg_buffercache_usage_counts()` (PG16+) are cheap aggregates.
- Most buffers with usagecount 5 and little free space: cache is too small for the working set.

## Warming after restart (pg_prewarm)
```sql
CREATE EXTENSION pg_prewarm;
SELECT pg_prewarm('orders');                       -- 'buffer' mode: into shared_buffers
SELECT pg_prewarm('orders_pkey');
SELECT pg_prewarm('big_table', 'prefetch');        -- async OS readahead into page cache only; ERROR "prefetch is not supported by this build" where the OS lacks posix_fadvise (Windows)
```
Prewarm the hot indexes first; they give the most hit-rate per MB.

## Automatic: autoprewarm
```ini
shared_preload_libraries = 'pg_prewarm'
pg_prewarm.autoprewarm = on            # default on once loaded
pg_prewarm.autoprewarm_interval = 300s
```
A background worker dumps the list of cached blocks to `autoprewarm.blocks` in the data directory every interval and at shutdown, and reloads them after startup. After failover the standby has its own cache state (it dumps its own file), which reflects replay activity rather than the primary's read pattern.

## Verify
```sql
SELECT autoprewarm_dump_now();     -- returns number of blocks written (errors while the autoprewarm worker holds the dump file, e.g. during a reload)
```
Compare `blks_hit / (blks_hit + blks_read)` in `pg_stat_database` during the first minutes after restart with and without prewarm.

## Gotchas
- Prewarming more than fits evicts what you just loaded; size the list to shared_buffers.
- `pg_buffercache_evict()` (PG17) exists for testing cold-cache behaviour; never on production hot paths.

## Checked
- PostgreSQL 17.6: `pg_prewarm` in `buffer`/`read` modes returned the block counts, `prefetch` failed on this Windows build with the quoted error; the buffer-cache query output has the listed columns, `pg_buffercache_summary()` and `pg_buffercache_usage_counts()` exist (the 16 docs list the summary function) and `pg_buffercache_evict()` evicted a buffer; with `shared_preload_libraries = 'pg_prewarm'` (a `postmaster` setting) `pg_prewarm.autoprewarm` is on, the interval default is 5 minutes, `autoprewarm.blocks` was written and a restart logged `autoprewarm successfully prewarmed N of M previously-loaded blocks`. The usagecount interpretation and hit-rate comparison are advice, not tested.
