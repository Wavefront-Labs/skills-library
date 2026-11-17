---
id: computing-software.database-administration.duckdb.duckdb-checkpoint-vacuum
name: duckdb-checkpoint-vacuum
category: computing-software
field: database-administration
product: duckdb
tags: [duckdb, checkpoint, vacuum, wal, reclaim-space, force-checkpoint]
level: practitioner
status: docs-checked
description: "Use CHECKPOINT and FORCE CHECKPOINT to flush the DuckDB WAL and reclaim deleted-row space; know what VACUUM does and does not do."
sources:
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/checkpoint.md
  - https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/1.4/sql/statements/vacuum.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: synchronise the write-ahead log (WAL) to the data file and recover space after deletes.

```sql
CHECKPOINT;            -- default database
CHECKPOINT file_db;    -- a specific attached database
FORCE CHECKPOINT;      -- see below
```

Checkpoints also run automatically based on WAL size (configuration). Plain `CHECKPOINT` fails if transactions are running. The Behavior section says `FORCE` aborts running transactions, but the examples section notes that in earlier versions `FORCE CHECKPOINT` aborted in-progress transactions and from v1.4 it waits until it can grab the checkpoint lock (and prevents new transactions from starting). The page does not reconcile the two statements.

Reclaiming space: after DELETE/TRUNCATE a checkpoint (automatic or manual) only partially reclaims space; it merges row groups with many deletes, which in the current implementation needs about 25% of rows deleted in adjacent row groups. It does not remove all deleted rows.

In-memory databases (new in v1.4.0): in-memory tables support checkpointing, which triggers vacuuming of deleted rows. They can also be compressed, which is off by default:

```sql
ATTACH ':memory:' AS memory_compressed (COMPRESS);
USE memory_compressed;
```
The Reclaiming Space section of the same page still says checkpointing has no effect in in-memory mode; that conflicts with the v1.4.0 section and the page does not reconcile them.

VACUUM is Postgres-compatibility only and its behaviour is likely to change. `VACUUM;` and `VACUUM ANALYZE;` are no-ops. `VACUUM my_table(my_column);` (or `VACUUM ANALYZE my_table(my_column);`) rebuilds distinct-count statistics. `VACUUM FULL` raises `Not implemented Error: Full vacuum option`. VACUUM does not reclaim space; a checkpoint partially does (see above).

## Checked

2026-11-07. Read the CHECKPOINT and VACUUM pages in full and confirmed the examples, automatic checkpoints by WAL size, failure with running transactions, the v1.4 FORCE note, the roughly 25 percent adjacent-row-group figure, in-memory checkpointing from v1.4.0 with COMPRESS, and the VACUUM no-ops, column form, `VACUUM FULL` error and no-reclaim warning. Rewrote the FORCE and in-memory paragraphs to state the page's own contradiction instead of advice to test, corrected the last VACUUM sentence (a checkpoint only partially reclaims) and removed the Verify step.

Method: documentation only; no commands were run.
