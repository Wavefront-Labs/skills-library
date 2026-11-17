---
id: computing-software.database-administration.mysql.hash-joins-index-merge-range-optimization
name: hash-joins-index-merge-range-optimization
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, hash-join-mysql, index-merge, range-optimization, block-nested-loop, join-buffer-size, explain]
level: practitioner
status: docs-checked
description: "Read and steer MySQL hash joins, index merge (union/intersection/sort-union) and range access, including join_buffer_size and range_optimizer_max_mem_size."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/hash-joins.html
  - https://dev.mysql.com/doc/refman/8.4/en/index-merge-optimization.html
  - https://dev.mysql.com/doc/refman/8.4/en/range-optimization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hash joins, index merge and range optimization

## Hash join (8.0.18+)
Used for equi-joins (and since 8.0.20 also non-equi and outer/semi/anti joins) when no usable index exists on the join column; replaced Block Nested Loop entirely in 8.0.20.
```sql
EXPLAIN FORMAT=TREE SELECT * FROM orders o JOIN legacy_codes c ON c.code = o.code;
-- -> Inner hash join (c.code = o.code)
--     -> Table scan on c
--     -> Hash
--         -> Table scan on o
```
- Build side kept in `join_buffer_size` memory (per join, per session); when exceeded it spills to disk in chunks. For a large reporting join, raise `join_buffer_size` for that session only (`SET SESSION join_buffer_size = 64*1024*1024`). Never raise it globally to hundreds of MB.
- Controls: the `hash_join` optimizer_switch flag has no effect in current 8.x releases; use hints `/*+ NO_BNL(t) */` / `/*+ BNL(t) */` to steer.
- A hash join on large tables is often a sign of a **missing index**; for OLTP add the index instead.

## Index merge
Combine several indexes on one table:
- `intersection`: `WHERE a = 1 AND b = 2` with separate indexes on a and b.
- `union`: `WHERE a = 1 OR b = 2`.
- `sort_union`: OR of range conditions.
```sql
EXPLAIN SELECT * FROM t WHERE a = 1 OR b = 2;   -- type: index_merge, Extra: Using union(idx_a,idx_b)
```
Intersection often means a composite index `(a, b)` would be better. Union is a good plan for OR conditions on different columns (otherwise rewrite as UNION ALL). Hints: `/*+ INDEX_MERGE(t idx_a, idx_b) */`, `/*+ NO_INDEX_MERGE(t) */`.

## Range optimization
- `IN (...)` lists use index dives up to `eq_range_index_dive_limit` (200) values, then switch to statistics estimates (cheaper, less accurate). Very large IN lists with skewed data may plan badly; consider a temporary table join.
- `range_optimizer_max_mem_size` (8 MB default): if a complex WHERE with many ranges exceeds it, the optimizer gives up on range access and does a **full scan**, with a warning `Memory capacity of ... for 'range_optimizer_max_mem_size' exceeded`. Check `SHOW WARNINGS` after EXPLAIN.
- Row constructor `(a, b) IN ((1,2),(3,4))` can use range access on a composite index.
- Skip scan: `WHERE b > 10` on index `(a, b)` with few distinct `a` values. Shows `Using index for skip scan`.

## Verify
`EXPLAIN ANALYZE` shows actual rows and time per iterator; compare chosen access with hints applied.

## Gotchas
- Hash join memory is per join operation; a query joining 6 tables can allocate several buffers.
- Index merge intersection can be slower than a single index scan when one condition is very selective; the optimizer sometimes misjudges with stale stats (run ANALYZE TABLE).

## Checked

2026-10-31: confirmed hash joins from MySQL 8.0.18, block nested loop support removed in 8.0.20, non-equi/outer/semi/anti join hash joins from 8.0.20, the hash_join optimizer_switch flag and HASH_JOIN/NO_HASH_JOIN hints having no effect since 8.0.19, join_buffer_size memory limits and disk spill, and BNL/NO_BNL steering (8.0/8.4 hash-join pages); the index merge algorithms (intersect/union/sort_union), EXPLAIN indicators, index_merge_* switch flags and INDEX_MERGE/NO_INDEX_MERGE hints; eq_range_index_dive_limit default 200, range_optimizer_max_mem_size default 8388608 with warning 3170, index dives vs statistics, row constructor IN range access, and skip scan with 'Using index for skip scan' and the skip_scan switch on the 8.4 range-optimization page. Removed the unconfirmed skip-scan and EXPLAIN ANALYZE version notes.
Method: documentation only; no commands were run.
