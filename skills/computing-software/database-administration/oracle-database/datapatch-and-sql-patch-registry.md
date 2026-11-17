---
id: computing-software.database-administration.oracle-database.datapatch-and-sql-patch-registry
name: datapatch-and-sql-patch-registry
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-patching, opatch, datapatch, dba-registry-sqlpatch, sql-patching, pdb-patching, utlrp]
level: advanced
status: gated
description: "Run Oracle datapatch after binary patching to apply SQL changes in the CDB and every PDB, read dba_registry_sqlpatch, and fix failed or pending SQL patch installs."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/26/dbpss/
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/DBA_REGISTRY_SQLPATCH.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# datapatch and the SQL patch registry

**Goal:** after OPatch updates the binaries, the data dictionary in every
container matches, and you can prove it.

## Why it exists
A Release Update changes binaries **and** SQL objects (PL/SQL packages,
dictionary views). OPatch only changes files in the Oracle home. datapatch runs
the SQL part in each database (and each PDB) and records it.

## Run
Unlike `opatchauto`, `opatch` does not run datapatch: run it yourself after the binaries are patched. Oracle's own example starts the database, opens the PDBs, then runs the sanity checks and the apply:
```sql
SQL> startup
SQL> alter pluggable database all open;
```
```bash
cd $ORACLE_HOME/OPatch
./datapatch -sanity_checks      # recommended by Oracle
./datapatch -verbose
```
Options `-pdbs` (select PDBs) and `-prereq` (preview) (gated: unconfirmed, source is paywalled or blocked). The datapatch user guide is My Oracle Support Doc ID 2680521.1, which needs a support login.
Behaviour of PDBs that were closed during datapatch or plugged in from an older home (gated: unconfirmed, source is paywalled or blocked).

## Read the registry
```sql
SELECT install_id, patch_id, patch_type, action, status, source_version, target_version, action_time, description
FROM dba_registry_sqlpatch ORDER BY action_time;
```
`action` is APPLY or ROLLBACK; `status` is SUCCESS or WITH ERRORS; `patch_type` is INTERIM, RU, RUI, RUR or CU; `logfile` names the log for that attempt. Verify that the APPLY row for the latest RU is SUCCESS. A `CDB_REGISTRY_SQLPATCH` view with `CON_ID` for all containers (gated: unconfirmed, source is paywalled or blocked).
Logs are under `$ORACLE_BASE/cfgtoollogs/sqlpatch/<patch#>/<unique id>`; the first lines of datapatch output say "Log file for this invocation:" and `sqlpatch_invocation.log` is in the same directory.

## When it fails
- `WITH ERRORS`: read the log named in the `logfile` column, fix the cause and rerun datapatch (retry behaviour, causes of failure and rollback procedure are in the Datapatch User Guide) (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Data Guard: which database runs datapatch and in what order (gated: unconfirmed, source is paywalled or blocked). OPatchAuto's Data Guard guide confirms only that opatch needs a manual datapatch.
- After opatch, datapatch runs against a started database: datapatch is not part of `opatch apply`.

## Verify
The registry shows SUCCESS for the APPLY of the RU in every container you run datapatch for.

## Checked
Date 2026-10-22. Oracle Database 19c Database Reference (DBA_REGISTRY_SQLPATCH), Oracle AI Database 26ai Single-Instance
Maintenance with OPatch, and OPatchAuto Data Guard guide as indexed by search. Confirmed: datapatch is run manually after
OPatch, `-sanity_checks` and `-verbose`, DBA_REGISTRY_SQLPATCH columns and value lists, log directory and invocation log.
Gated: datapatch `-pdbs`/`-prereq`, closed-PDB behaviour, CDB_REGISTRY_SQLPATCH, failure handling/rollback and the Data
Guard rule, because the Datapatch User Guide is a My Oracle Support document (Doc ID 2680521.1) that needs a login.
Removed: utlrp step, PDB_PLUG_IN_VIOLATIONS check, "closed PDBs are skipped" and failure-cause list.
Method: documentation only; no commands were run.
