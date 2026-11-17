---
id: computing-software.database-administration.oracle-database.unplugging-and-plugging-pdbs
name: unplugging-and-plugging-pdbs
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, multitenant, pluggable-database, unplug-pdb, plug-in-pdb, pdb-xml-manifest, pdb-archive, check-plug-compatibility, pdb-relocate, datapatch]
level: advanced
status: draft
description: "Move an Oracle PDB between CDBs by unplugging to an XML manifest or .pdb archive, checking compatibility, plugging in with COPY/NOCOPY/MOVE, or relocating online."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/unplugging-a-pdb.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/plugging-in-an-unplugged-pdb.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/multi/relocating-a-pdb.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unplugging and plugging PDBs

## Unplug
```sql
-- in the source CDB root
ALTER PLUGGABLE DATABASE sales CLOSE IMMEDIATE INSTANCES = ALL;
ALTER PLUGGABLE DATABASE sales UNPLUG INTO '/u01/stage/sales.xml';  -- manifest; datafiles stay in place
-- or a single archive with the datafiles inside (easy to copy):
ALTER PLUGGABLE DATABASE sales UNPLUG INTO '/u01/stage/sales.pdb';
DROP PLUGGABLE DATABASE sales KEEP DATAFILES;   -- removes it from the source CDB
```
An unplugged PDB cannot be opened in its source until dropped and re-plugged.
TDE: export the keys first (`ADMINISTER KEY MANAGEMENT EXPORT ENCRYPTION KEYS ... WITH SECRET`)
or use `UNPLUG INTO ... ENCRYPT USING '<secret>'` (12.2+), then import/`DECRYPT USING` on plug.

## Check compatibility on the target
```sql
SET SERVEROUTPUT ON
DECLARE ok BOOLEAN;
BEGIN
  ok := DBMS_PDB.CHECK_PLUG_COMPATIBILITY(pdb_descr_file => '/u01/stage/sales.xml', pdb_name => 'SALES');
  DBMS_OUTPUT.PUT_LINE(CASE WHEN ok THEN 'YES' ELSE 'NO' END);
END;
/
SELECT name, cause, type, message, status, action FROM pdb_plug_in_violations
WHERE name = 'SALES' AND status <> 'RESOLVED';
```
Typical violations: different patch level (needs `datapatch`), options installed in
source not in target, character set mismatch (target CDB must be AL32UTF8 or same),
parameter differences (warnings).

## Plug in
```sql
CREATE PLUGGABLE DATABASE sales USING '/u01/stage/sales.xml'
  NOCOPY TEMPFILE REUSE;                   -- use files where they are (same storage)
CREATE PLUGGABLE DATABASE sales USING '/u01/stage/sales.xml'
  COPY FILE_NAME_CONVERT = ('/u01/oradata/SRC/', '/u02/oradata/TGT/');   -- copy, keep source files
CREATE PLUGGABLE DATABASE sales USING '/u01/stage/sales.xml'
  MOVE FILE_NAME_CONVERT = ('/u01/oradata/SRC/', '/u02/oradata/TGT/');   -- move files
CREATE PLUGGABLE DATABASE sales USING '/u01/stage/sales.pdb';           -- archive; extracts files
-- AS CLONE when plugging the same PDB twice into one CDB (new GUID/DBID)
ALTER PLUGGABLE DATABASE sales OPEN;
```
If it opens `RESTRICTED`, read `PDB_PLUG_IN_VIOLATIONS`; usually run
`$ORACLE_HOME/OPatch/datapatch -verbose -pdbs SALES` (target on newer RU) then reopen.
Plugging into a higher version CDB requires an upgrade of the PDB:
`ALTER PLUGGABLE DATABASE sales OPEN UPGRADE;` then `dbupgrade -c SALES` (or AutoUpgrade).

## Online relocate (12.2+)
```sql
-- in the target CDB, with a db link to the source CDB root (user with SYSOPER/CREATE PLUGGABLE DATABASE)
CREATE PLUGGABLE DATABASE sales FROM sales@src_cdb_link RELOCATE AVAILABILITY MAX;
ALTER PLUGGABLE DATABASE sales OPEN;   -- the source closes and connections are forwarded
```
Requires local undo and ARCHIVELOG in the source; downtime is just the final open.

## Gotchas
- Back up the PDB in the target right after plugging: source RMAN backups belong to the
  source CDB (12.2+ "preplugin backups" can be used with `RESTORE ... FROM PREPLUGIN`).
- Services defined in the source CDB do not travel; recreate them with srvctl.
- `NOCOPY` with the source still using those files = corruption. Drop the source with KEEP DATAFILES first.

## Verify
- [ ] No unresolved rows in `PDB_PLUG_IN_VIOLATIONS`; `v$pdbs` shows READ WRITE, RESTRICTED = NO.
- [ ] New level 0 backup taken in the target CDB.
