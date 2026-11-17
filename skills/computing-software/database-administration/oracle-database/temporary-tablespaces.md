---
id: computing-software.database-administration.oracle-database.temporary-tablespaces
name: temporary-tablespaces
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-tablespaces, temporary-tablespace, tempfile, temporary-tablespace-group, ora-01652, v-tempseg-usage, sort-spill, local-temp-tablespace]
level: practitioner
status: docs-checked
description: "Manage Oracle temporary tablespaces and tempfiles: default temp, tablespace groups, local temporary tablespaces, checking free space, and approaching ORA-01652."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-tablespaces.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/V-TEMPSEG_USAGE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporary tablespaces

Temp holds spilled results of sorts, hash aggregations and joins, plus other temporary data.

## Create and assign
```sql
CREATE TEMPORARY TABLESPACE temp2 TEMPFILE '+DATA' SIZE 32G AUTOEXTEND ON NEXT 1G MAXSIZE 64G;
ALTER DATABASE DEFAULT TEMPORARY TABLESPACE temp2;   -- applies to users without an explicit temp
ALTER USER batch_user TEMPORARY TABLESPACE temp2;
SELECT property_value FROM database_properties WHERE property_name = 'DEFAULT_TEMP_TABLESPACE';
```
Users with no explicit temporary tablespace use the database default (`TEMP` for new installations).

A **tablespace group** lets one user consume temporary space from several tablespaces, and lets the parallel
execution servers of one parallel operation use multiple temporary tablespaces. A group is created implicitly by the
`TABLESPACE GROUP` clause, and can be set as the database default temporary tablespace:
```sql
ALTER TABLESPACE temp1 TABLESPACE GROUP tempgrp;
ALTER TABLESPACE temp2 TABLESPACE GROUP tempgrp;
ALTER DATABASE DEFAULT TEMPORARY TABLESPACE tempgrp;
```
**Local temporary tablespaces** (12.2 and later, `CREATE LOCAL TEMPORARY TABLESPACE`) keep separate, non-shared
temp files per instance and are used only for spilling SQL results that are visible only within that instance. An
ordinary temporary tablespace is the shared kind, on shared disk for all instances.

## Who is using temp now
`V$TEMPSEG_USAGE` shows temp segment use per session; `DBA_TEMP_FREE_SPACE` shows total allocated and free space
in each temporary tablespace:
```sql
SELECT * FROM dba_temp_free_space;
```

## ORA-01652 unable to extend temp segment
A single SQL needed more temp than available. Find the SQL and its plan first (a bad hash join or sort on a huge row
source, a Cartesian product, or stale statistics) before adding a tempfile.
`ALTER TABLESPACE temp ADD TEMPFILE '+DATA' SIZE 32G;`

## Shrinking temp
The Administrator's Guide has a section "Shrinking a Locally Managed Temporary Tablespace" for a temporary
tablespace with a large amount of unused space; follow it for the exact syntax.

## Verify
- [ ] Default temporary tablespace set (not SYSTEM) and alerts on temp usage.
- [ ] Top temp SQL reviewed after each ORA-01652, not just space added.

## Checked
2026-11-01. Confirmed against the Oracle 19c Administrator's Guide (Managing Tablespaces): default temp behaviour
and DEFAULT_TEMP_TABLESPACE, tablespace group purpose and implicit creation, local temporary tablespaces from 12.2,
DBA_TEMP_FREE_SPACE, existence of the shrink section. Corrected "18c+" to 12.2. Removed as unconfirmed: RMAN/recovery
behaviour of tempfiles, the V$TEMPSEG_USAGE join query, ASH history column, PGA advice, SHRINK SPACE syntax, DROP
TABLESPACE procedure, and per-PDB temp statement.
Method: documentation only; no commands were run.
