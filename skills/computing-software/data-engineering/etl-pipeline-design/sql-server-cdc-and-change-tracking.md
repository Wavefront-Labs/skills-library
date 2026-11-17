---
id: computing-software.data-engineering.etl-pipeline-design.sql-server-cdc-and-change-tracking
name: sql-server-cdc-and-change-tracking
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, sql-server-change-tracking, sql-server-cdc, cdc, debezium]
level: advanced
status: gated
description: "Capture changes from SQL Server with Change Tracking or CDC: enabling each, querying net changes, cleanup and retention, LSN/version bookmarks, and Debezium setup."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-tracking-sql-server
  - https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server
  - https://debezium.io/documentation/reference/stable/connectors/sqlserver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server CDC and Change Tracking

**Goal:** extract only changed rows from SQL Server, including deletes, without full scans.

## Change Tracking (CT): which rows changed
```sql
ALTER DATABASE Sales SET CHANGE_TRACKING = ON (CHANGE_RETENTION = 3 DAYS, AUTO_CLEANUP = ON);
ALTER TABLE dbo.Orders ENABLE CHANGE_TRACKING WITH (TRACK_COLUMNS_UPDATED = OFF);

DECLARE @last BIGINT = 41250;                         -- bookmark saved from the previous run
SELECT ct.SYS_CHANGE_OPERATION, ct.OrderID, o.*
FROM CHANGETABLE(CHANGES dbo.Orders, @last) ct
LEFT JOIN dbo.Orders o ON o.OrderID = ct.OrderID;     -- deletes have no row in Orders
SELECT CHANGE_TRACKING_CURRENT_VERSION();             -- save as next bookmark (read it consistently with the query)
```
- Lightweight, per Microsoft's Change Tracking article. The exact semantics, prerequisites (such as primary key) and isolation-level guidance are in that article; the T-SQL syntax above is from memory (gated: unconfirmed, source is paywalled or blocked).
- If `@last < CHANGE_TRACKING_MIN_VALID_VERSION(OBJECT_ID('dbo.Orders'))`, data was cleaned up: full reload needed.

## CDC: full change history from the log
```sql
EXEC sys.sp_cdc_enable_db;
EXEC sys.sp_cdc_enable_table @source_schema = N'dbo', @source_name = N'Orders', @role_name = NULL, @supports_net_changes = 1;
DECLARE @from binary(10) = sys.fn_cdc_get_min_lsn('dbo_Orders'), @to binary(10) = sys.fn_cdc_get_max_lsn();
SELECT * FROM cdc.fn_cdc_get_all_changes_dbo_Orders(@from, @to, N'all update old');
```
- The capture process reads the transaction log and uses SQL Server Agent (SQL Server, Managed Instance); there is built-in latency between commit and the change appearing. Azure SQL Database is covered by its own CDC article.
- Row metadata columns such as `__$start_lsn` and `__$operation` describe each change; look up the `__$operation` codes in the change-table documentation.
- Retention via the cleanup job (default three days); bookmark LSNs.
- The capture instance has a fixed column structure and ignores columns added later; plan a new capture instance for schema changes.

## Debezium
SQL Server connector reads CDC tables (CDC must be enabled), streams to Kafka with snapshot + streaming; tracks LSN offsets.

## Choosing
CT: simplest, low overhead, when you only need current values. CDC/Debezium: when you need every change or event streaming.

## Gotchas
- Read the CT version bookmark consistently with the change query so no rows fall between them (see the isolation guidance in the CT article).
- CDC adds log-reading work on high-write tables and has capture latency; monitor it.

## Verify
Insert/update/delete test rows; next extraction returns exactly those with correct operations, and bookmarks advance.

## Checked

2026-11-02. Confirmed against Microsoft Learn (About Change Tracking, About CDC) and the Debezium SQL Server connector page: CT is described as lightweight; CDC uses SQL Server Agent and the transaction log, has capture latency, default three-day retention, a fixed column structure per capture instance, `fn_cdc_get_min_lsn`/`fn_cdc_get_max_lsn`, and net-changes functions only when configured; Debezium works with CDC enabled, supports Azure SQL, and records LSNs. Removed: 'synchronous', primary-key requirement, snapshot-isolation advice, the numeric `__$operation` mapping and the Azure SQL scheduler remark, and the DMV recommendation, none of which the fetched pages state. Gated: the exact T-SQL statements and option names, because the fetched Microsoft pages do not show them.

Method: documentation only; no commands were run.
