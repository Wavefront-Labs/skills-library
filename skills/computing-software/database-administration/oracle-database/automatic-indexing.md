---
id: computing-software.database-administration.oracle-database.automatic-indexing
name: automatic-indexing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, automatic-indexing, dbms-auto-index, auto-index-mode, invisible-indexes, autonomous-database, exadata]
level: advanced
status: docs-checked
description: "Configure Oracle 19c+ automatic indexing with DBMS_AUTO_INDEX (report only vs implement), scope schemas, review the activity report, and drop or keep auto indexes."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-indexes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_AUTO_INDEX.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic indexing (DBMS_AUTO_INDEX)

Introduced in 19c. The 19c Licensing Information manual lists it as available only on Enterprise Edition on Exadata (EE-ES) and Exadata Database Service (ExaDB), not on plain EE or SE2; check the current Licensing Information for your release.
A background task captures workload SQL, creates candidate indexes, tests them against the captured SQL and makes them visible only if performance improves (new indexes are visible in IMPLEMENT mode, invisible in REPORT ONLY).

## Turn it on gradually
```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'REPORT ONLY');   -- new auto indexes are invisible and not used by SQL
-- review reports for a few weeks, then
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'IMPLEMENT');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_MODE', 'OFF');           -- stop; existing auto indexes remain
```

## Scope and limits
```sql
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_SCHEMA', 'SALES', allow => TRUE);    -- add to the inclusion list (case-sensitive name; allow => NULL removes it from either list)
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_SCHEMA', 'SCRATCH', allow => FALSE); -- exclude
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_DEFAULT_TABLESPACE', 'AUTO_IDX');
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_SPACE_BUDGET', '10');                 -- % of tablespace; only when the default tablespace is used for auto indexes
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_RETENTION_FOR_AUTO', '90');          -- drop unused auto indexes after N days (default 373)
EXEC DBMS_AUTO_INDEX.CONFIGURE('AUTO_INDEX_RETENTION_FOR_MANUAL', NULL);       -- NULL (the default) = never drop your manual indexes
SELECT parameter_name, parameter_value, last_modified FROM dba_auto_index_config;
```
Setting `AUTO_INDEX_RETENTION_FOR_MANUAL` to a number lets it drop **manual** indexes it considers unused: leave NULL unless intended.

## Review
```sql
SET LONG 1000000 PAGESIZE 0
SELECT DBMS_AUTO_INDEX.REPORT_ACTIVITY(SYSTIMESTAMP - 7, SYSTIMESTAMP, 'TEXT', 'ALL', 'ALL') FROM dual;
SELECT DBMS_AUTO_INDEX.REPORT_LAST_ACTIVITY() FROM dual;
SELECT owner, index_name, table_name, auto, visibility, status, tablespace_name FROM dba_indexes WHERE auto = 'YES';
```
`REPORT_ACTIVITY` sections: SUMMARY, INDEX_DETAILS, VERIFICATION_DETAILS, ERRORS or ALL (combine with + or -); type TEXT/HTML/XML; level BASIC/TYPICAL/ALL.

## Managing auto indexes
```sql
EXEC DBMS_AUTO_INDEX.DROP_AUTO_INDEXES('SALES', '"SYS_AI_8x2n5g0kk1q"', allow_recreate => FALSE);
EXEC DBMS_AUTO_INDEX.DROP_SECONDARY_INDEXES('SALES', 'ORDERS');   -- clean slate (drops non-constraint indexes!) for a fresh start
```
Auto indexes are flagged `AUTO = 'YES'` in `DBA_INDEXES`; drop them through the package. `DROP_SECONDARY_INDEXES` never drops indexes used for constraints; `DROP_AUTO_INDEXES(owner, index_name, allow_recreate)` defaults to `allow_recreate => FALSE`.

## Gotchas
- It works from SQL captured from the workload, so rarely run SQL may not be considered.
- The background task uses resources and can add load; review the activity reports (`REPORT_ACTIVITY`, `REPORT_LAST_ACTIVITY`).
- Index count grows; review space budget and retention.

## Verify
Report shows improved SQL with no regressions, and auto indexes stay within the space budget.

## Checked
Date 2026-10-22. Oracle Database 19c PL/SQL Packages and Types Reference (DBMS_AUTO_INDEX), Database Reference
(DBA_AUTO_INDEX_CONFIG, ALL_INDEXES.AUTO) and Licensing Information User Manual 19c. Confirmed: CONFIGURE parameter names,
modes, allow semantics, defaults (RETENTION_FOR_AUTO 373, RETENTION_FOR_MANUAL NULL), REPORT_ACTIVITY and
REPORT_LAST_ACTIVITY signatures, DROP_AUTO_INDEXES / DROP_SECONDARY_INDEXES signatures, availability (EE-ES and ExaDB only).
Corrected: availability was overstated (Oracle Cloud generally); removed the 15-minute cadence, SQL plan baseline claim,
dba_auto_index_executions view and "executed more than once" rule, none of which the documentation pages checked state.
Method: documentation only; no commands were run.
