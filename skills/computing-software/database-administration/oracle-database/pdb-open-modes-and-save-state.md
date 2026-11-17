---
id: computing-software.database-administration.oracle-database.pdb-open-modes-and-save-state
name: pdb-open-modes-and-save-state
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, multitenant, pluggable-database, pdb-save-state, alter-pluggable-database, open-modes, restricted-mode]
level: practitioner
status: docs-checked
description: "Open, close and restrict Oracle PDBs, make them reopen after CDB restart with SAVE STATE, and fix PDBs stuck in MOUNTED or RESTRICTED mode after patching."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/administering-pdbs-with-sql-plus.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/ALTER-PLUGGABLE-DATABASE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PDB open modes and SAVE STATE

## States
```sql
SHOW PDBS                                       -- SQL*Plus: CON_ID, CON_NAME, OPEN MODE, RESTRICTED
SELECT name, open_mode, restricted, open_time FROM v$pdbs;
```
Open modes: `MOUNTED` (closed), `READ WRITE`, `READ ONLY`. `RESTRICTED = YES`
means only users with `RESTRICTED SESSION` can connect.

## Commands (from CDB$ROOT)
```sql
ALTER PLUGGABLE DATABASE sales OPEN;
ALTER PLUGGABLE DATABASE sales OPEN READ ONLY;
ALTER PLUGGABLE DATABASE sales CLOSE IMMEDIATE;
ALTER PLUGGABLE DATABASE ALL OPEN;
ALTER PLUGGABLE DATABASE ALL EXCEPT pdb$seed CLOSE IMMEDIATE;
ALTER PLUGGABLE DATABASE sales OPEN RESTRICTED;
ALTER PLUGGABLE DATABASE sales OPEN INSTANCES = ALL;    -- RAC
```
From inside the PDB: `ALTER PLUGGABLE DATABASE OPEN;` / `SHUTDOWN IMMEDIATE` close only that PDB.

## Reopen automatically after CDB restart
By default PDBs come up `MOUNTED` after the CDB starts. Preserve the current state:
```sql
ALTER PLUGGABLE DATABASE sales SAVE STATE;          -- remembers READ WRITE
ALTER PLUGGABLE DATABASE ALL SAVE STATE;
ALTER PLUGGABLE DATABASE sales DISCARD STATE;
SELECT * FROM dba_pdb_saved_states;
```

## PDB opened RESTRICTED unexpectedly
Typical after patching, plugging or cloning. Check:
```sql
SELECT name, cause, type, message, status, action FROM pdb_plug_in_violations
WHERE status <> 'RESOLVED' ORDER BY time;
```
Common causes and fixes:
- SQL patch mismatch with CDB: run `datapatch` (with the PDB open).
- Component/option not installed in the CDB that the PDB uses.
- Character set or parameter incompatibility.
After fixing: `ALTER PLUGGABLE DATABASE sales CLOSE; ALTER PLUGGABLE DATABASE sales OPEN;`

## Gotchas
- `pdb$seed` is always READ ONLY; do not open it read write except under Oracle Support direction.

## Verify
After a CDB restart (`srvctl stop/start database` or `SHUTDOWN/STARTUP`), `SHOW PDBS` lists the
PDB `READ WRITE` with `RESTRICTED NO`, and applications connect via its service.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: SAVE STATE / DISCARD STATE and the DBA_PDB_SAVED_STATES view, ALL and ALL EXCEPT, the INSTANCES clause, OPEN READ WRITE [RESTRICTED] [FORCE], PDB$SEED READ ONLY, PDB_PLUG_IN_VIOLATIONS (Multitenant guide, ALTER PLUGGABLE DATABASE reference).

Removed or corrected: MIGRATE mode, saved-state column list, srvctl service advice, datapatch flags, CLOSE vs CLOSE IMMEDIATE behaviour and the RAC per-instance claim (not found in the cited pages).

Method: documentation only; no commands were run.
