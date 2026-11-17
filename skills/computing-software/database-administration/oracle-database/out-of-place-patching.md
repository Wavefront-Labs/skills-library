---
id: computing-software.database-administration.oracle-database.out-of-place-patching
name: out-of-place-patching
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, oracle-patching, opatch, out-of-place-patching, gold-image, new-oracle-home, minimal-downtime, autoupgrade-patching]
level: advanced
status: draft
description: "Patch Oracle by building a new, pre-patched Oracle home and moving the database to it with one restart, keeping the old home as an instant rollback."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/ladbi/about-out-of-place-patching.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/upgrd/using-autoupgrade-oracle-database-upgrades.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Out-of-place patching

**Goal:** downtime for a quarterly RU is one database restart, and rollback is
"start it from the old home".

## Procedure
1. **Build the new home** while production runs, e.g. `/u01/app/oracle/product/19.0.0/dbhome_19_25`:
   - install software only from the base image (or a gold image), with
     `runInstaller -applyRU <ru_dir>` to patch during installation, or
     install then `opatch apply` into the new home (nothing runs from it yet, so no downtime);
   - include one-off patches and the OJVM RU if used.
2. Copy configuration from the old home: `dbs/` (spfile/pfile, password file),
   `network/admin/` (or use a shared TNS_ADMIN), any `sqlnet.ora` wallet references, `/etc/oratab` entry update planned.
3. **Switch** (downtime starts):
   ```bash
   srvctl stop database -d ORCL                         # or SHUTDOWN IMMEDIATE
   srvctl modify database -d ORCL -oraclehome /u01/app/oracle/product/19.0.0/dbhome_19_25   # Oracle Restart/RAC
   # update /etc/oratab, environment ORACLE_HOME
   srvctl start database -d ORCL
   $NEW_HOME/OPatch/datapatch -verbose
   ```
   Move the listener too if it runs from the old home.
4. Keep the old home until the next cycle: rollback = stop, point back, start,
   and run datapatch from the old home (it rolls back SQL changes).

## Automation
- AutoUpgrade (recent versions) has a patching mode that downloads RUs, builds the new home and moves the database.
- Fleet Patching and Provisioning / gold images (`runInstaller -createGoldImage`) for many servers.

## Gotchas
- Disk: an Oracle home is ~8-15 GB; keep at least two.
- Hard-coded paths in scripts, cron, monitoring agents and `TNS_ADMIN` break after the switch: grep for the old home.
- RAC: rolling out-of-place is possible per node with `srvctl` services relocation.

## Verify
`srvctl config database -d ORCL` (or the `pmon` process's binary path,
`ls -l /proc/<pmon-pid>/exe`) shows the new home, `opatch lspatches` in the new home lists the RU, and `dba_registry_sqlpatch` shows the RU as SUCCESS.
