---
id: computing-software.database-administration.oracle-database.adding-and-deleting-rac-nodes
name: adding-and-deleting-rac-nodes
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, add-node-rac, delete-node, gridsetup, addnode-sh, grid-infrastructure, srvctl]
level: sme
status: docs-checked
description: "Extend an Oracle RAC cluster to a new node (Grid home, DB home, instance) and remove a node cleanly, with the pre-checks and srvctl steps in the right order."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/adding-and-deleting-cluster-nodes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/adding-and-deleting-oracle-rac-from-nodes-on-linux-and-unix-systems.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding and deleting RAC nodes

## Add a node
Prepare node3 identically: OS, packages, kernel parameters, users/groups with the same UIDs/GIDs,
SSH equivalence for grid and oracle, shared storage visible (ASM disks with same names/permissions),
public, private (interconnect) and VIP addresses in DNS/hosts.

1. Check from an existing node (grid user, `Grid_home/bin`): `cluvfy comp peer -n node3 -verbose` compares the new node
   with a reference node; the guide documents `cluvfy stage -pre nodeadd -n node3 [-fixup] [-verbose]` in its Windows
   steps and the same stage is the usual pre-check on Linux.
2. Extend Grid Infrastructure (19c, from an existing node's grid home):
   ```bash
   $GRID_HOME/gridSetup.sh -silent -addNodes -responseFile ... \
     "CLUSTER_NEW_NODES={node3}" "CLUSTER_NEW_VIRTUAL_HOSTNAMES={node3-vip}"
   # older/alternate: $GRID_HOME/addnode/addnode.sh -silent "CLUSTER_NEW_NODES={node3}" "CLUSTER_NEW_VIRTUAL_HOSTNAMES={node3-vip}"
   ```
   Then run `orainstRoot.sh` and `root.sh` on node3 as root when prompted.
   `cluvfy stage -post nodeadd -n node3`; `crsctl stat res -t` shows node3 resources ONLINE.
3. Extend the database home (oracle user, from an existing node):
   ```bash
   $ORACLE_HOME/addnode/addnode.sh -silent "CLUSTER_NEW_NODES={node3}"
   # then Oracle_home/root.sh on node3 as root; open PDBs on the new node (ALTER PLUGGABLE DATABASE pdb_name OPEN)
   ```
4. Add the instance (from any node):
   ```bash
   dbca -silent -addInstance -nodeName node3 -gdbName ORCL -instanceName ORCL3 \
     -sysDBAUserName sys -sysDBAPassword "<SECRET>"
   ```
   DBCA adds the redo thread, undo tablespace, instance parameters and registers with clusterware.
5. Services: add node3's instance as preferred or available for each service with `srvctl modify service` (syntax in the Oracle RAC Administration and Deployment Guide), and run any needed PDB open steps.

## Delete a node
1. Relocate services away; remove the instance:
   ```bash
   srvctl stop instance -db ORCL -instance ORCL3
   dbca -silent -deleteInstance -nodeList node3 -gdbName ORCL -instanceName ORCL3 -sysDBAUserName sys -sysDBAPassword "<SECRET>"
   ```
   (removes thread and undo; `-nodeList` is only needed when deleting from a node other than the one running DBCA).
   Relocate services first so the instance is neither preferred nor available for any service. For policy-managed
   databases use `srvctl stop instance -db db_unique_name -node node_name` then `srvctl relocate server`. Confirm
   the redo thread is gone in `GV$LOG` (else `ALTER DATABASE DISABLE THREAD n;`).
2. Remove the DB home from node3: stop/disable a listener running from that home
   (`srvctl disable listener -l listener_name -n node3`, `srvctl stop listener ...`), then on node3 run
   `$ORACLE_HOME/deinstall/deinstall -local` (not for a shared home: it would remove the shared software).
3. Remove from the cluster (root on a remaining node, after `crsctl stop crs` / deconfig on node3):
   ```bash
   $GRID_HOME/crs/install/rootcrs.sh -deconfig -force     # on node3, as root
   crsctl delete node -n node3                             # on node1, as root
   ```
   For a non-shared Grid home run `Grid_home/deinstall/deinstall -local` on node3 (shared home: `rootcrs.sh -deconfig -force`
   then `runInstaller -detachHome ORACLE_HOME=Grid_home -silent -local`). Run `crsctl unpin css` first if `olsnodes -s -t`
   shows the node pinned. Then `cluvfy stage -post nodedel -n node3`, and remove the node's VIP if it remains
   (`srvctl config vip -node node3`, `srvctl stop vip -vip vip_name`, `srvctl remove vip -vip vip_name`).

## Gotchas
- `olsnodes -s -t` shows pinned/unpinned and status; `crsctl unpin css` first if the node is pinned.
- Remember monitoring, backups, oratab and cron on the new node.

## Checked
Date 2026-10-22. Oracle Database 19c Clusterware Administration and Deployment Guide (cwadd) and RAC Administration
and Deployment Guide (racad). Confirmed: DBCA `-addInstance`/`-deleteInstance` options, database-home `addnode.sh`
syntax, `rootcrs.sh -deconfig -force`, `crsctl delete node -n` run as root from a surviving node, `cluvfy stage -post
nodeadd`/`-post nodedel`, `deinstall -local` and the shared-home caveat. Removed: `gridSetup.sh -addNodes`
(not documented), a Linux `runInstaller -updateNodeList` step (documented only for Windows).
Method: documentation only; no commands were run.

## Verify
`olsnodes -n -s` lists the expected nodes, `srvctl status database -db ORCL` shows all instances running, services balanced.
