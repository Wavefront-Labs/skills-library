---
id: computing-software.database-administration.oracle-database.table-compression
name: table-compression
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, table-compression-oracle, advanced-compression, basic-compression, hybrid-columnar-compression, compression-advisor, dbms-compression]
level: advanced
status: docs-checked
description: "Choose and apply Oracle table compression (basic, advanced row, hybrid columnar), estimate ratios with DBMS_COMPRESSION, and compress existing data."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-tables.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_COMPRESSION.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/vldbg/partition-table-compression.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table compression

## Types
| Type | Syntax | Compressed when |
|---|---|---|
| Basic | `ROW STORE COMPRESS BASIC` (same as `ROW STORE COMPRESS`) | only bulk load or array insert; other inserts and updated rows stay uncompressed |
| Advanced row | `ROW STORE COMPRESS ADVANCED` | single-row inserts and updates too, once a block reaches a database-controlled threshold; direct-path loads compress immediately |
| Warehouse (Hybrid Columnar) | `COLUMN STORE COMPRESS FOR QUERY [LOW\|HIGH]` | direct-path or array insert; `QUERY HIGH` is the default |
| Archive (Hybrid Columnar) | `COLUMN STORE COMPRESS FOR ARCHIVE [LOW\|HIGH]` | direct-path or array insert; `ARCHIVE LOW` is the default |
Direct-path methods that compress immediately: direct-path SQL*Loader, `CREATE TABLE AS SELECT`, parallel INSERT, and
INSERT with `APPEND` or `APPEND_VALUES`. Updates and conventional inserts on Hybrid Columnar data move rows to row
format and lower the compression level; ADO policies can move them back. Hybrid Columnar methods have higher CPU
overhead than basic or advanced row compression, and `QUERY HIGH` is described as performing well on Exadata storage.
Compression can be set on a tablespace (default for new tables), a table or a partition.

## Estimate first
```sql
DECLARE
  l_blkcnt_cmp PLS_INTEGER; l_blkcnt_uncmp PLS_INTEGER; l_row_cmp PLS_INTEGER; l_row_uncmp PLS_INTEGER;
  l_ratio NUMBER; l_type VARCHAR2(100);
BEGIN
  DBMS_COMPRESSION.GET_COMPRESSION_RATIO(
    scratchtbsname => 'USERS', ownname => 'SALES', objname => 'ORDERS', subobjname => NULL,
    comptype => DBMS_COMPRESSION.COMP_ADVANCED,
    blkcnt_cmp => l_blkcnt_cmp, blkcnt_uncmp => l_blkcnt_uncmp,
    row_cmp => l_row_cmp, row_uncmp => l_row_uncmp, cmp_ratio => l_ratio, comptype_str => l_type);
  DBMS_OUTPUT.PUT_LINE(l_type || ' ratio ' || ROUND(l_ratio, 2));
END;
/
```
The procedure builds its analysis tables in the scratch tablespace and does not modify your table.

## Apply
```sql
-- new data only
ALTER TABLE sales.orders ROW STORE COMPRESS ADVANCED;
-- new and existing data in one partition
ALTER TABLE sales.orders MOVE PARTITION p_2024_01 COLUMN STORE COMPRESS FOR QUERY HIGH;
-- policy-based: row-level tiering from the Administrator's Guide
ALTER TABLE oe.orders ILM ADD POLICY COLUMN STORE COMPRESS FOR QUERY ROW AFTER 14 DAYS OF NO MODIFICATION;
```
Per partition: `MODIFY PARTITION ... COMPRESS ...` changes new data only; `MOVE PARTITION ... COMPRESS ...` or online
table redefinition changes new and existing data. A partition's setting overrides the table's. To convert Hybrid
Columnar data back: `ALTER TABLE table_name MOVE ROW STORE COMPRESS ADVANCED;`.

## Check
```sql
SELECT table_name, partition_name, compression, compress_for FROM dba_tab_partitions WHERE table_owner = 'SALES';
SELECT DBMS_COMPRESSION.GET_COMPRESSION_TYPE('SALES','ORDERS', rowid) FROM sales.orders WHERE ROWNUM <= 10;
```
For non-partitioned tables `COMPRESSION` is `ENABLED` in `*_TABLES` and `COMPRESS_FOR` shows the method.

## Gotchas
- `ALTER TABLE ... COMPRESS` alone does not compress existing data; a `MOVE` does.
- These methods do not apply to SecureFiles LOBs, which have their own compression.
- Check which methods your edition, option licences and storage platform allow before using advanced row or
  Hybrid Columnar compression.

## Verify
Segment size drops by the estimated ratio and key queries are no slower in a before/after test.

## Checked
2026-11-09. Confirmed against the 19c Administrator's Guide (managing tables: table compression methods, partition
compression, ILM examples), the `DBMS_COMPRESSION` reference and the VLDB partitioning page (partition-level
inheritance of compression from table or tablespace, compression changes during `MOVE PARTITION`). Removed as not stated on those pages: the licensing column and the
`dba_feature_usage_statistics` note, the "10-50x" ratio, `MOVE ONLINE` and 12.2 version claims, index
`REBUILD ... COMPRESS ADVANCED LOW`, `UPDATE INDEXES` and UNUSABLE-index notes, the 90-day ILM example, the
Exadata offload and CPU-on-DML remarks, and the `dba_segments` query.
Method: documentation only; no commands were run.
