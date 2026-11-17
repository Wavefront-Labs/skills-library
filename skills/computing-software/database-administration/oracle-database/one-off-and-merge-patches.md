---
id: computing-software.database-administration.oracle-database.one-off-and-merge-patches
name: one-off-and-merge-patches
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, one-off-patch, merge-patch, opatch, monthly-recommended-patches, datapatch, patch-conflict, overlay-patch]
level: advanced
status: draft
description: "Apply Oracle one-off and merge patches on top of a Release Update: conflict checks, requesting merges, Monthly Recommended Patches, online patches, and datapatch."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/opatc/index.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/datapatch-sql-patching.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# One-off and merge patches

A **one-off** (interim) patch fixes one bug for a specific RU. Two one-offs that touch the same
files conflict; Oracle then provides a **merge** patch (one patch containing both fixes) built for your RU.
**Monthly Recommended Patches (MRP)** (19.17+ on Linux) bundle recommended one-offs on top of an RU,
reducing ad-hoc requests.

## Before downloading
- Exact RU: `$ORACLE_HOME/OPatch/opatch lspatches` and `SELECT * FROM dba_registry_sqlpatch ORDER BY action_time;`.
- Download the one-off for that RU and platform (the patch README lists the base release).
- Latest OPatch (patch 6880880) unzipped into `$ORACLE_HOME/OPatch`.

## Conflict check
```bash
cd /stage/34567890
$ORACLE_HOME/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
$ORACLE_HOME/OPatch/opatch prereq CheckSystemSpace -ph ./
```
Conflict output names the installed patch it clashes with. Options: request a merge patch on MOS
(Patch Conflict Analysis tool, or an SR with the `opatch lsinventory` output), or check whether a
newer RU/MRP already contains both fixes (often the better answer).
Superset patch (contains the installed one): OPatch rolls back the subset automatically.

## Apply (single instance)
```bash
# stop everything from the home: database, listener (if from this home)
$ORACLE_HOME/OPatch/opatch apply
# start the database (all PDBs open), then the SQL part
$ORACLE_HOME/OPatch/datapatch -verbose
```
Many one-offs are SQL-free, but run datapatch anyway; it is idempotent. Online patches
(`opatch apply online -connectString orcl:sys:<SECRET>:`) exist for some bugs (README says "online patch").
RAC / Grid: `opatchauto apply /stage/34567890` as root, node by node (rolling if the README says so).

## Out-of-place with one-offs
Build a new home: install RU via `runInstaller -applyRU <ru_dir> -applyOneOffs <p1>,<p2>` (gold image), switch
the database to it, run datapatch. Keeps rollback trivial and the old home intact.

## Check the result
```bash
$ORACLE_HOME/OPatch/opatch lspatches
```
```sql
SELECT patch_id, patch_type, action, status, description FROM dba_registry_sqlpatch ORDER BY action_time DESC;
SELECT con_id, patch_id, status FROM cdb_registry_sqlpatch WHERE status <> 'SUCCESS';
```
All PDBs SUCCESS; invalid objects compiled (`@?/rdbms/admin/utlrp.sql`).

## Rollback
`opatch rollback -id 34567890`, then `datapatch -verbose` (rolls back the SQL part).

## Gotchas
- One-offs are tied to an RU: next quarter's RU needs the matching one-off version (or it is included). Track them in a patch inventory.
- Patching a home used by several databases patches them all at the binary level; datapatch must run in each.
- PDBs closed while datapatch ran are not patched: open them and run datapatch again, then check `cdb_registry_sqlpatch`.

## Verify
Patch in `lspatches`, SQL registry SUCCESS for every container, the bug reproduction test passes.
