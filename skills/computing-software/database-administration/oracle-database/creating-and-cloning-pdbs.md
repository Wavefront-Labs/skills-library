---
id: computing-software.database-administration.oracle-database.creating-and-cloning-pdbs
name: creating-and-cloning-pdbs
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, multitenant, pluggable-database, cdb, create-pluggable-database, pdb-clone, hot-clone, refreshable-pdb, pdb-seed]
level: advanced
status: draft
description: "Create Oracle PDBs from the seed, hot-clone local or remote PDBs over a database link, and use refreshable clones for test copies, with the open/save-state steps people forget."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/creating-and-removing-pdbs-with-sql-plus.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-PLUGGABLE-DATABASE.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creating and cloning PDBs

**Goal:** new or copied pluggable databases in minutes, opened automatically
after restarts.

## From the seed
```sql
-- connected to CDB$ROOT as SYSDBA (OMF via db_create_file_dest makes FILE_NAME_CONVERT unnecessary)
CREATE PLUGGABLE DATABASE salespdb
  ADMIN USER pdbadmin IDENTIFIED BY "<secret>" ROLES = (DBA)
  DEFAULT TABLESPACE users DATAFILE SIZE 1G AUTOEXTEND ON
  STORAGE (MAXSIZE 200G);
ALTER PLUGGABLE DATABASE salespdb OPEN;
ALTER PLUGGABLE DATABASE salespdb SAVE STATE;     -- reopen automatically when the CDB restarts
```
Without SAVE STATE (or a startup trigger), PDBs come up MOUNTED after a CDB restart.

## Local hot clone (12.2+, source stays open read-write)
Requires local undo mode (`SELECT property_value FROM database_properties WHERE property_name='LOCAL_UNDO_ENABLED';`) and ARCHIVELOG.
```sql
CREATE PLUGGABLE DATABASE sales_test FROM salespdb;
ALTER PLUGGABLE DATABASE sales_test OPEN;
```

## Remote clone over a database link
```sql
-- in source CDB: common user with CREATE PLUGGABLE DATABASE privilege
CREATE USER c##clone IDENTIFIED BY "<secret>" CONTAINER=ALL;
GRANT CREATE SESSION, CREATE PLUGGABLE DATABASE TO c##clone CONTAINER=ALL;
-- in target CDB
CREATE DATABASE LINK src_link CONNECT TO c##clone IDENTIFIED BY "<secret>" USING 'srchost:1521/CDB1';
CREATE PLUGGABLE DATABASE sales_copy FROM salespdb@src_link PARALLEL 8;
```
Same endianness required; target version >= source (a lower version clone
needs upgrade; open with `UPGRADE` and run AutoUpgrade/dbupgrade).

## Refreshable clone (test copies kept current)
```sql
CREATE PLUGGABLE DATABASE sales_rpt FROM salespdb@src_link REFRESH MODE EVERY 60 MINUTES;
ALTER PLUGGABLE DATABASE sales_rpt OPEN READ ONLY;
-- manual refresh: close it, then ALTER PLUGGABLE DATABASE sales_rpt REFRESH;
```
Can later be converted (`REFRESH MODE NONE`) for a near-zero-downtime relocate.

## Gotchas
- Licensing: more than 3 user PDBs per CDB (19c+) needs the Multitenant option.
- `PDB_PLUG_IN_VIOLATIONS` explains why a PDB opens in RESTRICTED mode.
- TDE: cloning encrypted PDBs needs `KEYSTORE IDENTIFIED BY` clause and keys exported/available.

## Verify
```sql
SHOW PDBS;
SELECT con_name, instance_name, state FROM dba_pdb_saved_states;
SELECT name, cause, message, status FROM pdb_plug_in_violations WHERE status <> 'RESOLVED';
```
