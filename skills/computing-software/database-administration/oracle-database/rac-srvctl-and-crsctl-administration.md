---
id: computing-software.database-administration.oracle-database.rac-srvctl-and-crsctl-administration
name: rac-srvctl-and-crsctl-administration
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, oracle-database, rac, real-application-clusters, srvctl, crsctl, clusterware, grid-infrastructure, scan-listener, olsnodes]
level: advanced
status: docs-checked
description: "Operate an Oracle RAC cluster day to day with srvctl (databases, instances, services, listeners) and crsctl (clusterware stack and resource health)."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/server-control-utility-reference.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/oracle-clusterware-control-crsctl-utility-reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAC administration with srvctl and crsctl

**Goal:** start, stop and inspect a RAC database through the clusterware, never
around it.

## Rule
Clusterware-managed resources must be controlled with `srvctl` (from the
database home, as oracle) so the cluster registry (OCR) knows the intended
state. `SHUTDOWN` in SQL*Plus works but clusterware may restart the instance or
report it as failed.

## srvctl: database resources
```bash
srvctl status database -db ORCL
srvctl stop instance -db ORCL -instance ORCL2 -stopoption IMMEDIATE     # take one node out
srvctl start instance -db ORCL -instance ORCL2
srvctl stop database -db ORCL -stopoption IMMEDIATE      # all instances
srvctl config database -db ORCL
srvctl status scan_listener ; srvctl status listener
srvctl modify database -db ORCL -policy AUTOMATIC
```
Services (where applications connect):
```bash
srvctl add service -db ORCL -service sales_svc -preferred ORCL1 -available ORCL2 -failovertype TRANSACTION -commit_outcome TRUE
srvctl start service -db ORCL -service sales_svc
srvctl relocate service -db ORCL -service sales_svc -oldinst ORCL1 -newinst ORCL2 -drain_timeout 60
```

## crsctl: clusterware itself (often as root / grid)
```bash
crsctl check cluster -all            # CRS, CSS, EVM on every node
crsctl stat res -t                   # all resources, target vs state, per node
crsctl stop crs                      # stop whole stack on this node (root) before OS patching
crsctl start crs
crsctl query crs activeversion ; crsctl query css votedisk
olsnodes -n -s                       # nodes and status
```

## Gotchas
- `crsctl stat res -t` showing `TARGET=ONLINE STATE=OFFLINE` = clusterware wants
  it up and failed to start it; check the resource's alert/trace (ADR under the grid base).
- Node evictions come from CSS heartbeats (network) or voting disk I/O misses;
  the clusterware logs and the OS log hold the reason.
- Use `-drain_timeout` with service stop/relocate so sessions finish first.

## Verify
`srvctl status database -db ORCL` lists all instances running; `crsctl stat res -t`
has no OFFLINE resources with target ONLINE.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: srvctl option names -db, -instance, -stopoption, -service, -failovertype, -commit_outcome, -drain_timeout, -policy; crsctl check cluster and crsctl stat res (Real Application Clusters Administration and Deployment Guide, srvctl and crsctl reference).

Removed or corrected: legacy short flags -d/-i/-o/-s were replaced by the documented -db/-instance/-stopoption/-service forms; -v and the config comment and the ocssd.trc file name removed (not found in the cited pages).

Method: documentation only; no commands were run.
