---
id: computing-software.database-administration.oracle-database.segment-advisor-and-shrinking-segments
name: segment-advisor-and-shrinking-segments
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-tablespaces, datafiles, segment-advisor, shrink-space, row-movement, alter-table-move-online, high-water-mark, reclaim-space, datafile-resize, dbms-advisor]
level: advanced
status: docs-checked
description: "Find reclaimable space in Oracle with the Segment Advisor, reclaim it with SHRINK SPACE or ALTER TABLE MOVE ONLINE, and then resize datafiles below the HWM."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-space-for-schema-objects.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment Advisor and shrinking segments

**Goal:** get space back after large deletes or purges, where it is worth the effort.
Deleting rows frees space inside the segment for new inserts, but the high-water mark
(HWM) and datafile sizes stay; full scans still read up to the HWM.

## Find candidates: automatic Segment Advisor
The Automatic Segment Advisor is a maintenance task that runs in all maintenance windows. It examines AWR usage and growth statistics and samples segment data, but you cannot change which tablespaces and segments it selects. Latest results, with the suggested command in `c1`:
```sql
SELECT tablespace_name, segment_name, segment_type, partition_name, recommendations, c1
FROM TABLE(DBMS_SPACE.ASA_RECOMMENDATIONS('FALSE','FALSE','FALSE'));
```
Manual run for one object (`recommend_all` defaults to TRUE: findings for all specified segments):
```sql
DECLARE tname VARCHAR2(100) := 'seg_orders'; oid NUMBER; tid NUMBER;
BEGIN
  DBMS_ADVISOR.CREATE_TASK('Segment Advisor', tid, tname);
  DBMS_ADVISOR.CREATE_OBJECT(tname, 'TABLE', 'APP', 'ORDERS', NULL, NULL, oid);
  DBMS_ADVISOR.SET_TASK_PARAMETER(tname, 'RECOMMEND_ALL', 'TRUE');
  DBMS_ADVISOR.EXECUTE_TASK(tname);
END;
/
SELECT f.message, f.more_info FROM dba_advisor_findings f WHERE f.task_name = 'seg_orders';
```

## Reclaim: SHRINK SPACE (online, locally managed ASSM tablespaces only)
```sql
ALTER TABLE app.orders ENABLE ROW MOVEMENT;
ALTER TABLE app.orders SHRINK SPACE COMPACT;   -- phase 1: defragment and compact rows, HWM not reset yet
ALTER TABLE app.orders SHRINK SPACE CASCADE;   -- phase 2 (reissue without COMPACT): reset HWM; CASCADE also shrinks dependent indexes
ALTER INDEX app.orders_ix1 SHRINK SPACE;
ALTER TABLE app.orders MODIFY LOB (doc) (SHRINK SPACE);
```
Without `COMPACT` the shrink does both phases in one go; `COMPACT` suits long-running queries that might read reclaimed blocks. Shrink invalidates cursors (reparse) unless `COMPACT` is used, and can invalidate dependent objects.
Rows move to new locations, so enable row movement first and disable any rowid-based triggers.
Not eligible even in an ASSM tablespace: IOT mapping tables, tables with rowid-based materialized views, tables with function-based indexes, SECUREFILE LOBs, and tables using basic compression (`ROW STORE COMPRESS BASIC`), warehouse compression (`COLUMN STORE COMPRESS FOR QUERY`) or archive compression. Tables with `ROW STORE COMPRESS ADVANCED` are eligible.

## Reclaim: ALTER TABLE MOVE ONLINE
Relocates the table (or a partition) into a new segment, optionally in another tablespace; `ONLINE` allows DML on the table during the move:
```sql
ALTER TABLE app.orders MOVE ONLINE TABLESPACE app_data;
ALTER TABLE app.orders MOVE PARTITION p2024 ONLINE UPDATE INDEXES;
```
A new segment needs free space for the copy. Restrictions of moving a table online: it cannot be combined with other clauses in the same statement, is not allowed for a partitioned index-organized table, and not when a domain index (spatial, XML, Text) exists on the table. The Segment Advisor recommends online table redefinition for tables that cannot be shrunk (for example in a non-ASSM tablespace).

## Then shrink the datafile
Space freed inside a tablespace returns to the OS only if no extent sits above the new size:
```sql
SELECT file_id, MAX(block_id + blocks) AS last_block   -- multiply by the tablespace block size
FROM dba_extents WHERE tablespace_name = 'APP_DATA' GROUP BY file_id;
ALTER DATABASE DATAFILE 12 RESIZE 40G;   -- fails if extents lie above the new size
```
Find what sits at the end with `dba_extents WHERE file_id = 12 ORDER BY block_id DESC`
(`file_id`, `block_id` and `blocks` are `DBA_EXTENTS` columns) and move those segments first.

## Verify
- [ ] `dba_segments.bytes` dropped for the target objects; indexes VALID.
- [ ] Datafile resized and filesystem/ASM free space increased.
- [ ] No rowid-based triggers or rowid-based materialized views depend on the table before enabling row movement.

## Checked
2026-10-31. Against the Oracle Database 19c Administrator's Guide (Managing Space for Schema Objects), the SQL Language Reference (ALTER TABLE, move_table_clause) and the Database Reference (DBA_EXTENTS): Automatic Segment Advisor behaviour, `DBMS_SPACE.ASA_RECOMMENDATIONS` columns, `DBMS_ADVISOR` task and object calls and `recommend_all`, shrink eligibility list, `COMPACT` and `CASCADE` semantics, row movement and rowid-trigger requirement, `MOVE ONLINE` restrictions and `DBA_EXTENTS` columns. Removed unconfirmed details: `ORA-03297`, the "12.2+" version gate, Advanced Compression licensing remark, `DBMS_REDEFINITION` name, `ALTER TABLESPACE ... SHRINK SPACE` and 23ai `DBMS_SPACE.SHRINK_TABLESPACE` remarks, the "BASICFILE only" LOB note, and redo/undo volume claim.
Method: documentation only; no commands were run.
