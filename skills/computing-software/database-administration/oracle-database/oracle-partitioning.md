---
id: computing-software.database-administration.oracle-database.oracle-partitioning
name: oracle-partitioning
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-partitioning, interval-partitioning, reference-partitioning, partition-maintenance, exchange-partition, local-index, partition-pruning]
level: advanced
status: docs-checked
description: "Partition Oracle tables (range, interval, list, hash, reference, composite), choose local vs global indexes, and run partition maintenance online."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/partition-create-tables-indexes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/maintenance-partition-tables-indexes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/partition-pruning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle partitioning

Partitioning option (Enterprise Edition). Benefits: pruning (queries read only relevant
partitions), manageability (drop/exchange/compress per partition), availability.

## Interval (range that creates partitions automatically)
```sql
CREATE TABLE sales.orders (
  order_id NUMBER, order_date DATE NOT NULL, customer_id NUMBER, amount NUMBER)
PARTITION BY RANGE (order_date) INTERVAL (NUMTOYMINTERVAL(1, 'MONTH'))
(PARTITION p_before_2025 VALUES LESS THAN (DATE '2025-01-01'));
```
New months get system-named partitions (`SYS_P1234`) on first insert. Rename for sanity:
`ALTER TABLE sales.orders RENAME PARTITION FOR (DATE '2026-10-15') TO p_2026_10;`
Store-in rotation: `STORE IN (ts1, ts2)`.

## Others
- **List**: `PARTITION BY LIST (region) (PARTITION p_eu VALUES ('DE','FR'), PARTITION p_def VALUES (DEFAULT))`; `AUTOMATIC` list creates partitions for new values (it needs at least one partition at creation and cannot have a DEFAULT partition).
- **Hash**: spread hot inserts/large joins.
- **Reference**: child inherits the parent's partitioning via an enabled and enforced foreign key (the child key column is declared NOT NULL):
  ```sql
  CREATE TABLE sales.order_lines (line_id NUMBER, order_id NUMBER NOT NULL,
    CONSTRAINT fk_ol FOREIGN KEY (order_id) REFERENCES sales.orders(order_id))
  PARTITION BY REFERENCE (fk_ol);
  ```
  You cannot drop a partition of a reference-partitioned table directly; a drop on the parent cascades to the descendant tables.
- **Composite**: range-hash, interval-list, etc.

## Indexes
- **Local**: one index partition per table partition; maintenance on one partition affects only its index partition. Default choice.
- **Global (partitioned or not)**: needed for unique keys not containing the partition key; partition DDL makes them UNUSABLE unless `UPDATE INDEXES`; with asynchronous global index maintenance, DROP PARTITION ... UPDATE INDEXES is metadata only and global indexes stay valid.

## Maintenance
```sql
ALTER TABLE sales.orders DROP PARTITION p_2023_01 UPDATE INDEXES;
ALTER TABLE sales.orders TRUNCATE PARTITION FOR (DATE '2024-01-15') UPDATE INDEXES;
ALTER TABLE sales.orders MOVE PARTITION p_2024_01 TABLESPACE archive COMPRESS UPDATE INDEXES;
ALTER TABLE sales.orders SPLIT PARTITION p_before_2025 AT (DATE '2024-01-01') INTO (PARTITION p_old, PARTITION p_2024) UPDATE INDEXES;
ALTER TABLE sales.orders MERGE PARTITIONS p_2024_01, p_2024_02 INTO PARTITION p_2024_q1 UPDATE INDEXES;
-- load: exchange a staged table in as a partition, metadata only
ALTER TABLE sales.orders EXCHANGE PARTITION p_2026_10 WITH TABLE sales.orders_stage INCLUDING INDEXES WITHOUT VALIDATION;
```
Online options (`ONLINE` on MOVE, SPLIT, MERGE, or converting a non-partitioned table) are release-dependent: look them up in the SQL Language Reference for your version before use.

## Check pruning
Read the plan (`EXPLAIN PLAN`, `DBMS_XPLAN`): the partition rows with Pstart/Pstop show which partitions are read; a scan of all partitions means no pruning (often a function on the partition key or a bind type mismatch).

## Inspect
```sql
SELECT partition_name, high_value, num_rows, compression, tablespace_name FROM dba_tab_partitions
WHERE table_owner = 'SALES' AND table_name = 'ORDERS' ORDER BY partition_position;
```

## Verify
Key queries show pruning in their plans and the monthly purge/archive job runs in seconds.

## Checked
2026-11-01. Confirmed against the Oracle 19c VLDB and Partitioning Guide pages (creating partitioned tables and indexes; maintenance): automatic list partitioning rules, reference partitioning constraint, drop cascade on reference-partitioned tables, UPDATE INDEXES behaviour and asynchronous global index maintenance on DROP PARTITION. Removed: version gates (12c, 12.2), powers-of-2 hash advice, ONLINE clauses and online conversion, specific plan operator names.
Method: documentation only; no commands were run.
