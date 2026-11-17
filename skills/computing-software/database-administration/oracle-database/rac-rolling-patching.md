---
id: computing-software.database-administration.oracle-database.rac-rolling-patching
name: rac-rolling-patching
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, real-application-clusters, rolling-patch, opatchauto, grid-infrastructure, release-update, out-of-place-patching, datapatch, oracle-patching, drain-timeout, fleet-patching]
level: sme
status: draft
description: "Apply Oracle Grid and database Release Updates node by node in RAC with opatchauto, draining services first, then run datapatch once, keeping the database open throughout."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/upgrading-patching-downgrading-oracle-data-guard-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling patching in RAC

**Goal:** apply a Release Update (RU) to Grid Infrastructure and the database homes
with the database available the whole time: one node down at a time, services drained.

## Preconditions
- Patch README says "RAC Rolling Installable" (RUs and most one-offs are; some are not).
- Latest OPatch in every home (`$ORACLE_HOME/OPatch/opatch version`; unzip new OPatch over the old).
- Conflict check and space check on each node:
```bash
$GRID_HOME/OPatch/opatchauto apply /stage/RU_19_25 -analyze
```
- Services defined with `-preferred/-available` so every service has somewhere to run
  while a node is down; applications use FAN-aware pools (see RAC services skill).
- Backups of homes (tar or out-of-place clone) and the inventory.

## In-place, node by node (opatchauto)
On node 1, as root:
```bash
# move work off the node with a drain first
srvctl stop instance -db orcl -node node1 -drain_timeout 300 -stopoption IMMEDIATE -failover
$GRID_HOME/OPatch/opatchauto apply /stage/RU_19_25      # patches GI + DB homes on this node, restarts stack
```
opatchauto stops the CRS stack on that node, patches the Grid home and every DB home
it manages, and restarts. Then repeat on node 2..n. Meanwhile the other nodes serve the
database. Check after each node:
```bash
crsctl query crs activeversion -f     # cluster upgrade state ROLLING PATCH until the last node
crsctl query crs softwarepatch        # patch level of this node
$ORACLE_HOME/OPatch/opatch lspatches
srvctl status database -db orcl
```

## Out-of-place (preferred for less downtime per node and easy rollback)
Install new homes with the RU pre-applied (gold image or `runInstaller -applyRU`),
then per node: switch the GI home (`gridSetup.sh -switchGridHome` in 19c) and move the
database to the new DB home (`srvctl modify database -db orcl -oraclehome <new_home>`
then restart instances one at a time). Fleet Patching and Provisioning (FPP) automates this
(`rhpctl move gihome`, `rhpctl move database ... -batches`).

## After the last node: datapatch once
SQL changes apply to the database dictionary, not per node, so run on one node only
after all homes are patched:
```bash
$ORACLE_HOME/OPatch/datapatch -verbose            # all open PDBs, CDB root first
```
```sql
SELECT patch_id, action, status, description, action_time FROM dba_registry_sqlpatch ORDER BY action_time;
SELECT name, open_mode, restricted FROM v$pdbs;   -- RESTRICTED = YES often means datapatch missing in that PDB
```

## Rollback
Same rolling sequence with `opatchauto rollback` (in-place) or switching back to the old
homes (out-of-place), then `datapatch -verbose` to roll back SQL changes.

## Gotchas
- Mixed patch levels are allowed only during the rolling window; finish it the same day.
- `ROLLING PATCH` state blocks some cluster changes; `crsctl stop rollingpatch` only if Support says so.
- Data Guard: patch standby first (standby-first patching for RUs), then primary; datapatch on primary only.
- Check `opatchauto` logs under `$GRID_BASE/crsdata/<node>/crsconfig` and `cfgtoollogs/opatchauto` on failure;
  `opatchauto resume` continues after fixing the cause.

## Verify
- [ ] `crsctl query crs activeversion -f` shows NORMAL state and the new patch level on all nodes.
- [ ] `opatch lspatches` identical across nodes and homes.
- [ ] `dba_registry_sqlpatch` shows SUCCESS for the RU in root and every PDB.
