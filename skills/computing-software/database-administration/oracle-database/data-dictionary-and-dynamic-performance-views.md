---
id: computing-software.database-administration.oracle-database.data-dictionary-and-dynamic-performance-views
name: data-dictionary-and-dynamic-performance-views
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, dynamic-performance-views, data-dictionary, v-dollar-views, dba-views, gv-views]
level: practitioner
status: docs-checked
description: "Use Oracle's data dictionary (USER/ALL/DBA views) and dynamic performance views (V$/GV$): what each is, when it is available, and its limits."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/data-dictionary-and-dynamic-performance-views.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/about-dynamic-performance-views.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data dictionary and dynamic performance views

## Two families
| Family | What it is | Available |
|---|---|---|
| Data dictionary (`USER_`, `ALL_`, `DBA_`) | read-only base tables owned by SYS plus views that decode them | whenever the database is open (stored in the SYSTEM tablespace) |
| Dynamic performance (`V$`, `GV$`) | virtual views over memory structures, not conventional tables | depends on state: see below |

## Data dictionary
- `DBA_` views show all relevant information in the database and are for administrators. `ALL_` views show objects the
  user owns or has been granted access to, and obey the currently enabled roles (so `SET ROLE NONE` can change the
  row count, and stored procedures, where roles are not enabled by default, can see less). `USER_` views show objects
  the user owns and usually omit the `OWNER` column.
- Not every set has all three: there is a `DBA_LOCK` view but no `ALL_LOCK`.
- `SELECT * FROM DICTIONARY` lists the data dictionary views with short comments; the Oracle Database Reference has
  the full list.
- Never change rows or objects in the SYS schema; only Oracle should write the base tables. Program against the public
  synonyms rather than the base tables, which are more likely to change between releases.
- `DBMS_METADATA` extracts complete object definitions as XML or SQL DDL.
- `DUAL` has one column `DUMMY` and one row, `X`.

## Dynamic performance views
- SYS owns the underlying `V_$` objects; public synonyms with the `V$` prefix are what you query. Use only `V$`.
- `V$FIXED_TABLE` lists the dynamic performance tables and views.
- Availability: after the instance starts, views that read from memory work (for example `V$INSTANCE` and
  `V$BGPROCESS` before mount). Views that read from disk need the database mounted, and some need it open
  (`V$DATAFILE` needs a mounted database).
- Only simple queries are supported. For sorts, joins or `GROUP BY`, copy the data into a table first
  (`CREATE TABLE ... AS SELECT`) and query that. Read consistency is not guaranteed.
- After installation only SYS or SYSDBA can access the underlying dynamic performance tables; grant access to others
  deliberately. `catalog.sql` creates the views and synonyms (DBCA runs it).
- For almost every `V$` view there is a `GV$` view. In RAC it returns data from all qualified instances and adds an
  `INST_ID` column you can filter on, for example `SELECT * FROM GV$LOCK WHERE INST_ID = 2 OR INST_ID = 5;`.
- `V$` and `GV$` views are `CONTAINER_DATA` objects. Queried from the root, results depend on the user's
  `CONTAINER_DATA` attribute (set with `ALTER USER ... CONTAINER_DATA`), and data from PDBs is converted to the root
  character set (AL32UTF8), which can truncate columns that are too narrow.

## Verify
A monitoring account can run the dictionary and `V$` queries you rely on, and long-running monitoring queries copy
`V$` data to a table before joining or aggregating.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Database Concepts chapter "Data Dictionary and Dynamic
Performance Views" and the Database Reference page "About Dynamic Performance Views" (both read in full). Removed (not
stated there): the "what to query for common questions" table of view names, `CDB_` views and `CON_ID` scoping, the
licensing remark about Diagnostics Pack views, `SELECT_CATALOG_ROLE` advice, `v$fixed_view_definition` query,
`v$sql` cost remark.
Method: documentation only; no commands were run.
