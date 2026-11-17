---
id: computing-software.database-administration.oracle-database.rac-one-node-and-online-relocation
name: rac-one-node-and-online-relocation
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, rac-one-node, online-relocation, srvctl-relocate, omotion, grid-infrastructure, failover]
level: advanced
status: docs-checked
description: "Run Oracle RAC One Node: single active instance with cold failover and online relocation between nodes, conversion to and from full RAC, and patching with relocation."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/administering-oracle-rac-one-node.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/server-control-utility-reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAC One Node and online relocation

A RAC One Node database runs **one** instance on one node of a cluster. If the node fails,
clusterware restarts the instance on another candidate node (cold failover, minutes). For planned
maintenance, **online relocation** starts a second instance on the target node, migrates sessions,
then shuts down the original: near-zero downtime.

## Create / inspect
DBCA: database type "Oracle RAC One Node database", choose candidate servers. Or convert:
```bash
srvctl convert database -db ORCL -dbtype RACONENODE -instance ORCL_1 -timeout 30
srvctl config database -db ORCL
srvctl status database -db ORCL
```
At least one service besides the default is required; clients connect via SCAN and the service.

## Online relocation
```bash
srvctl relocate database -db ORCL -node node2 -timeout 30 -verbose
srvctl status database -db ORCL        # shows the relocation state during the move
```
- A temporary second instance opens on node2; services move; sessions are migrated
  (FAN-aware pools and TAF/Application Continuity move cleanly; others are disconnected at the end of the timeout).
- `-timeout` (minutes) is how long the old instance waits for sessions to drain before shutting down abort-style for leftovers.

## Patching with relocation
Rolling patch of the cluster: relocate the database off node1, patch node1, relocate back (or onward),
patch node2. Database binaries patched out-of-place on each node keep the same pattern; run datapatch once after all nodes are done.

## Convert to full RAC and back
```bash
srvctl convert database -db ORCL -dbtype RAC -node node1   # then add instances (srvctl add instance / dbca -addInstance)
srvctl convert database -db ORCL -dbtype RACONENODE -instance ORCL_1   # from RAC: only one instance must be running/configured
```
Useful for temporarily scaling out during peaks if licensing allows.

## Gotchas
- Online relocation needs enough memory on the target to briefly run both instances (one per node, but SGA on the target must fit).
- Failover is restart, not transparent: in-flight transactions roll back; clients need retry/Application Continuity.

## Verify
`srvctl relocate` completes within the timeout in a test, applications log only FAN events (no errors), and `srvctl config database` lists the expected candidate servers.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: srvctl convert database ... -dbtype RACONENODE [-instance] [-timeout], online relocation and the online relocation timeout (Real Application Clusters Administration and Deployment Guide, Administering Oracle RAC One Node).

Removed or corrected: licensing remark, candidate-server modify command, -abort, 720-minute maximum, relocation status text and the instance-name-suffix gotcha (not found in the cited pages).

Method: documentation only; no commands were run.
