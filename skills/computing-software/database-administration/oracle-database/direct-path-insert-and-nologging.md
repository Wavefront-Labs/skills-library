---
id: computing-software.database-administration.oracle-database.direct-path-insert-and-nologging
name: direct-path-insert-and-nologging
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, direct-path-insert, nologging, append-hint, ctas, force-logging, parallel-dml, unrecoverable]
level: advanced
status: docs-checked
description: "Load Oracle data fast with direct-path INSERT /*+ APPEND */, CTAS and NOLOGGING, and handle the consequences for backups, Data Guard and locking."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-tables.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/types-parallelism.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/managing-oracle-data-guard-physical-standby-databases.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct-path insert, CTAS and NOLOGGING

## Direct path
Writes formatted blocks above the high-water mark, bypassing the buffer cache and generating
minimal undo for the table data.
```sql
INSERT /*+ APPEND */ INTO sales.orders_hist SELECT * FROM sales.orders WHERE order_date < DATE '2025-01-01';
COMMIT;   -- required before the same session can read or modify the table again (ORA-12838)

-- array inserts from PL/SQL / apps
INSERT /*+ APPEND_VALUES */ INTO t VALUES (:1, :2);

-- parallel direct path
ALTER SESSION ENABLE PARALLEL DML;
INSERT /*+ APPEND PARALLEL(t, 8) */ INTO sales.orders_hist t SELECT /*+ PARALLEL(s, 8) */ * FROM sales.orders s;
```
Locking: direct-path insert takes an exclusive table lock (or partition lock with partition-extended syntax): no concurrent DML.

## CTAS
```sql
CREATE TABLE sales.orders_2024 NOLOGGING PARALLEL 8 COMPRESS AS
SELECT * FROM sales.orders WHERE order_date >= DATE '2024-01-01' AND order_date < DATE '2025-01-01';
ALTER TABLE sales.orders_2024 LOGGING NOPARALLEL;
```

## NOLOGGING
With the segment (or tablespace) NOLOGGING, direct-path operations generate almost no redo for the data.
Conventional DML always logs. Consequences:
- The blocks are **unrecoverable** from backups taken before the load: media recovery marks them
  corrupt. Take a backup of the affected datafiles right after.
- Physical standbys get nonlogged (invalid) blocks, listed in `V$NONLOGGED_BLOCK`.
```sql
SELECT * FROM v$nonlogged_block;   -- on a standby
```
Data Guard environments: `ALTER DATABASE FORCE LOGGING;` (overrides NOLOGGING; standard for DG).
18c+ alternatives: `ALTER DATABASE SET STANDBY NOLOGGING FOR LOAD PERFORMANCE;` or `FOR DATA AVAILABILITY`. Repair standby after NOLOGGING: `RECOVER DATABASE NONLOGGED BLOCK;` (18c+) on the standby or restore files from the primary.

## Gotchas
- Indexes on the target are maintained at the end of a direct-path load (sorts in temp): drop/mark unusable and rebuild for very large loads.
- APPEND on small frequent inserts wastes space (each insert starts above the HWM) and serialises sessions.

## Verify
After a NOLOGGING load, a fresh backup of the affected datafiles exists and `V$NONLOGGED_BLOCK` on the standby is empty.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: APPEND and APPEND_VALUES direct-path methods, ORA-12838 until COMMIT, parallel DML via ALTER SESSION ENABLE PARALLEL DML, FORCE LOGGING, SET STANDBY NOLOGGING FOR LOAD PERFORMANCE / FOR DATA AVAILABILITY, RECOVER ... NONLOGGED BLOCK, V$NONLOGGED_BLOCK (Administrator Guide; Data Guard Concepts; RMAN reference).

Removed or corrected: fall-back conditions and plan operation names, ORA-01578/ORA-26040 attributions, v$datafile unrecoverable columns and REPORT UNRECOVERABLE, the asynchronous-shipping remark and the foreign-key workaround (not found in the cited pages).

Method: documentation only; no commands were run.
