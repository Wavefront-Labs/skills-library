---
id: computing-software.database-administration.query-optimisation.hash-and-sort-spills-to-disk
name: hash-and-sort-spills-to-disk
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, hash-batches, work-mem-spill, sort-spill, memory-grant, execution-plans]
level: practitioner
status: gated
description: "Spot sorts and hash joins/aggregates spilling to disk in execution plans (PostgreSQL work_mem batches, SQL Server spill warnings, MySQL sort buffers) and fix them."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM
  - https://www.postgresql.org/docs/current/using-explain.html
  - https://learn.microsoft.com/en-us/sql/relational-databases/event-classes/hash-warning-event-class
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash and sort spills to disk

## Recognise
PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`:
```text
Sort Method: external merge  Disk: 812345kB          -- sort spilled
Hash  Buckets: 65536  Batches: 32  Memory Usage: 4097kB   -- Batches > 1 = hash spilled
HashAggregate ... Batches: 5  Memory Usage: 4145kB  Disk Usage: 210000kB   -- PG13+
```
The `external merge  Disk:` and `Disk Usage:` line formats above are from memory (gated: unconfirmed, source is paywalled or blocked); the EXPLAIN page shows `Sort Method: quicksort  Memory:` and `Batches: 1` for the in-memory case.
SQL Server: the Hash Warning event class reports hash recursion and hash bailout (build input does not fit in memory); check the execution plan for spill warnings.
MySQL: check the server's sort and temporary-table status counters and the manual for your version.

## Why it hurts
Disk I/O for intermediate data, multiple passes, and in hash joins recursive batching. Often 10x slower than in-memory.

## Fixes (in order)
1. **Reduce rows/width first**: filter earlier, select fewer columns (wide rows fill memory), aggregate before joining.
2. **Fix estimates**: spills often happen because the optimiser expected 1,000 rows and got 1M (memory sized for the estimate). Update statistics, extended statistics.
3. **Give the query more memory, locally**:
```sql
SET LOCAL work_mem = '256MB';      -- PostgreSQL, inside the transaction for this query only
```
`work_mem` defaults to 4MB. `hash_mem_multiplier` (default 2.0 in the current docs) multiplies `work_mem` to give the hash-table limit; the docs suggest raising it where spilling is routine and raising `work_mem` alone causes memory pressure. Do not raise global `work_mem` blindly: a complex query can run several sort and hash operations at once, each allowed that much memory, and concurrent sessions multiply it again.
SQL Server: for hash recursion and bailout the docs advise checking and updating statistics on joined/grouped columns, using a different join type, or adding memory.
MySQL: tune the sort and temporary-table buffers per session; confirm the variable names in the manual for your version.
4. **Avoid the sort**: an index providing the order (ORDER BY ... LIMIT), or pre-aggregated tables.

## Monitoring
PostgreSQL: `log_temp_files = 0` logs every temporary file with its size when it is deleted; `pg_stat_database.temp_bytes` (total data written to temporary files per database) trends. Queries with recurring temp files are tuning candidates.

## Verify
Plan shows `Sort Method: quicksort Memory:` / `Batches: 1` and execution time drops; temp file logs disappear for that query.

## Checked

- Date: 2026-11-02.
- Confirmed against: PostgreSQL docs for work_mem (default 4MB, several operations at once), hash_mem_multiplier (default 2.0, multiplies work_mem), log_temp_files (0 logs all temporary files), pg_stat_database.temp_bytes and EXPLAIN (Sort Method quicksort, Batches: 1); Microsoft Learn Hash Warning event class (hash recursion, bailout and the advice list).
- Removed: SQL Server sort_warning, hash_spill_details, total_spills, memory grant feedback and MIN_GRANT_PERCENT claims; MySQL variable and counter names; the PG13 version gate.
- Gated: the exact `Sort Method: external merge  Disk:` and `Disk Usage:` output formats (the fetched EXPLAIN page shows only in-memory examples).

Method: documentation only; no commands were run.
