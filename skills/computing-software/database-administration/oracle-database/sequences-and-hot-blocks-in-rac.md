---
id: computing-software.database-administration.oracle-database.sequences-and-hot-blocks-in-rac
name: sequences-and-hot-blocks-in-rac
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, sequence-cache-rac, scalable-sequences, hot-blocks, right-hand-index-growth, gc-buffer-busy, reverse-key-index]
level: advanced
status: docs-checked
description: "Fix Oracle RAC contention from sequences and right-growing indexes: sequence CACHE/NOORDER, scalable sequences, reverse-key and hash-partitioned indexes."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-SEQUENCE.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/design-and-deployment-techniques.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequences and hot blocks in RAC

## Symptoms
AWR (RAC sections) on insert-heavy workloads: top waits `gc buffer busy acquire/release`
and `gc current block busy`.
Segments by global cache buffer busy point at a primary key index on an ID column.

## Sequences
Every `NEXTVAL` that exhausts the cache updates the sequence's dictionary row, which all instances share.
```sql
SELECT * FROM dba_sequences WHERE sequence_owner = 'APP';
ALTER SEQUENCE app.order_seq CACHE 1000 NOORDER;
```
- **CACHE**: the default is too small for busy RAC sequences; use a large cache. Gaps on
  instance restart/shared pool flush are normal and should not matter (sequences never guarantee gap-free).
- **ORDER** forces global ordering across instances (cross-instance messaging on every call): avoid
  unless the business truly requires strict ordering; use timestamps for ordering instead.
- Each instance gets its own cache range, so values from node1 and node2 interleave as ranges (1..1000, 1001..2000).

## The index hot block
Values from a monotonically increasing sequence all land in the right-most leaf block of the PK
index. With several instances inserting, that block ships back and forth constantly.
Options:
1. **Scalable sequences (18c+)**: prefix values with instance and session digits, spreading inserts across the index.
   Use the `SCALE` clause of `CREATE SEQUENCE` / `ALTER SEQUENCE` (see the SQL Language Reference).
   Values become much larger (wider numbers); check column precision.
2. **Large CACHE + NOORDER** already spreads instances into separate ranges (node1 inserts into one region, node2 another) once caches are big.
3. **Reverse-key index**: spreads inserts but kills index range scans on the key; acceptable only for equality lookups.
4. Service affinity: route the insert workload to one instance (singleton service) so no inter-instance pinging happens.

## Also check
- Small hot lookup tables updated by all nodes: consider partitioning by instance or redesign (counter tables).

## Verify
After the change, AWR shows `gc buffer busy` and `enq: SQ` dropping for the workload, and insert throughput scales with instances.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: scalable sequences from Oracle Database 18c, CACHE with NOORDER recommended for sequence performance, gc buffer busy statistic (Administrator Guide, Real Application Clusters guide).

Removed or corrected: enq: SQ and dc_sequences waits, default cache size and suggested range, the SCALE EXTEND statement and scale_flag column, hash-partitioned index option and ASSM/freelist remark (not found in the cited pages).

Method: documentation only; no commands were run.
