---
id: computing-software.database-administration.oracle-database.opatch-inventory-conflicts-and-rollback
name: opatch-inventory-conflicts-and-rollback
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-patching, opatch, lsinventory, opatch-rollback, prereq-conflict-check, oracle-inventory]
level: practitioner
status: draft
description: "Check what is installed in an Oracle home with opatch lsinventory, run conflict and space prerequisite checks before patching, and roll back a patch cleanly."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/opatc/opatch-utility.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/opatc/opatch-commands.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OPatch inventory, conflict checks and rollback

## Use a current OPatch
Every Release Update readme states a minimum OPatch version. Replace `$ORACLE_HOME/OPatch`
with the latest from patch 6880880 before anything else:
```bash
$ORACLE_HOME/OPatch/opatch version
cd $ORACLE_HOME && mv OPatch OPatch.$(date +%F) && unzip -q /stage/p6880880_190000_Linux-x86-64.zip
```

## What is installed
```bash
$ORACLE_HOME/OPatch/opatch lspatches                 # one line per patch: id;description
$ORACLE_HOME/OPatch/opatch lsinventory               # full detail, bugs fixed, Oracle home info
$ORACLE_HOME/OPatch/opatch lsinventory -detail
```
Database side (what datapatch applied to the SQL dictionary):
```sql
SELECT patch_id, action, status, description, action_time FROM dba_registry_sqlpatch ORDER BY action_time;
```
Binary inventory and SQL registry must agree after patching; mismatches mean datapatch was not
run (or failed) in some database/PDB.

## Prerequisite checks (run on every node before the window)
```bash
cd /stage/36233263          # unzipped patch directory
$ORACLE_HOME/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
$ORACLE_HOME/OPatch/opatch prereq CheckSystemSpace -ph ./
```
- Conflicts with installed one-off patches: Oracle Support provides a **merge patch** or a
  version of the one-off on top of the new RU (use the Patch Conflict Checker on MOS with your
  lsinventory output).
- Space: the RU backs up replaced files under `$ORACLE_HOME/.patch_storage`; tens of GB.
  `opatch util cleanup` removes storage of superseded patches (not needed for rollback of the
  current one).

## Apply (single instance)
```bash
srvctl stop database -d PROD          # or shutdown; all processes from the home must stop
$ORACLE_HOME/OPatch/opatch apply -silent /stage/36233263
srvctl start database -d PROD
$ORACLE_HOME/OPatch/datapatch -verbose
```

## Roll back
```bash
srvctl stop database -d PROD
$ORACLE_HOME/OPatch/opatch rollback -id 36233263
srvctl start database -d PROD
$ORACLE_HOME/OPatch/datapatch -verbose        # rolls back the SQL changes too
```
For RUs, rolling back returns the home to the previous RU only if its files are in
`.patch_storage`. **Out-of-place** patching (new home, switch databases over) makes rollback
just a switch back and is preferred for production.

## Gotchas
- Check `fuser`/`lsof` on `$ORACLE_HOME/lib` if apply complains files are busy (listener,
  agent, ASM from the same home).
- Central inventory (`/u01/app/oraInventory`, see `/etc/oraInst.loc`) must be writable and
  consistent; a corrupt inventory makes OPatch fail.
- Grid Infrastructure homes use `opatchauto`, not plain `opatch apply`.

## Verify
`opatch lspatches` lists the RU, `dba_registry_sqlpatch` shows `SUCCESS` for it in every
container, and `SELECT * FROM v$version;` reports the new release.
