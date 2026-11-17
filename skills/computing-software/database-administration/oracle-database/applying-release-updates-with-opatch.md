---
id: computing-software.database-administration.oracle-database.applying-release-updates-with-opatch
name: applying-release-updates-with-opatch
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-patching, opatch, release-update, ru, opatch-prereq, oracle-home, quarterly-patching]
level: advanced
status: docs-checked
description: "Apply an Oracle quarterly Release Update to a single-instance home with OPatch: prerequisite checks, conflict detection, apply, datapatch, and verification."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/26/dbpss/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Applying a Release Update with OPatch

**Goal:** the database home is on the current quarterly RU with security fixes,
applied the same way every quarter.

## Release Updates
Release Updates are cumulative: the latest RU contains all earlier RUs for that release. Follow Oracle's published
Critical Patch Update schedule for dates. Each RU README (on My Oracle Support) states the minimum
OPatch version and any special steps: read it first.

## Procedure (in-place, single instance)
1. Update OPatch in the home:
   ```bash
   mv $ORACLE_HOME/OPatch $ORACLE_HOME/OPatch.old && unzip -q p6880880_<release>_<platform>.zip -d $ORACLE_HOME
   $ORACLE_HOME/OPatch/opatch version
   ```
2. Back up the home (tar) and have a database backup.
3. Unzip the RU, check conflicts:
   ```bash
   cd /stage/<RU_patch_id>
   $ORACLE_HOME/OPatch/opatch prereq CheckConflictAgainstOHWithDetail -ph ./
   ```
   The report lists conflicting and superset patches; resolve conflicts per Doc ID 1321267.1 (My Oracle Support) before applying.
4. Stop **everything** running from that home: databases, listeners, agents
   (`lsnrctl stop`, `srvctl stop home` for Restart/RAC).
5. Apply from inside the unzipped patch directory: `$ORACLE_HOME/OPatch/opatch apply`.
6. Start the listener and database (`startup`; for CDB open all PDBs: `alter pluggable database all open;`).
7. Apply SQL changes (unlike opatchauto, opatch does not run datapatch for you): `cd $ORACLE_HOME/OPatch && ./datapatch -sanity_checks` (recommended by Oracle) then `./datapatch -verbose` (see datapatch skill).
   Check `APPLY` rows in `dba_registry_sqlpatch` show `SUCCESS`.

## Gotchas
- Leaving any process from the home running makes OPatch fail with files in use (`fuser` on files under the home finds culprits).
- Grid Infrastructure homes are patched with `opatchauto` as root, not plain opatch (Oracle's opatchauto guides).
- In-place patching = downtime for the whole home; out-of-place patching (new home, switch) shortens it. Prefer that for production.
- Check the RU README for companion patches (for example OJVM if Java in the database is used).

## Verify
```bash
$ORACLE_HOME/OPatch/opatch lspatches
```
```sql
SELECT patch_id, action, status, description, action_time FROM dba_registry_sqlpatch ORDER BY action_time;
SELECT comp_id, version_full, status FROM dba_registry;   -- all VALID
```

## Checked
Date 2026-10-22. Oracle AI Database 26ai Single-Instance Maintenance with OPatch (dbpss), and Oracle's OPatch syntax
reference (12.1) for `-ph`. Confirmed: `opatch prereq CheckConflictAgainstOHWithDetail -ph ./`, apply from the patch
directory with the home's database and listeners shut down, manual datapatch after OPatch (`-sanity_checks`,
`-verbose`), `dba_registry_sqlpatch` APPLY = SUCCESS, RUs are cumulative. Removed (not confirmed): month list of RU
releases, `CheckSystemSpace`, utlrp step, patch id example. Old source URL (19/opatch/) returned 404.
Method: documentation only; no commands were run.
