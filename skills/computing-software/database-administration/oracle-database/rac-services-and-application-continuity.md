---
id: computing-software.database-administration.oracle-database.rac-services-and-application-continuity
name: rac-services-and-application-continuity
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, services, srvctl, application-continuity, transaction-guard, fan, drain-timeout, planned-maintenance]
level: advanced
status: docs-checked
description: "Define Oracle RAC services for Application Continuity and Transaction Guard with srvctl, use FAN and the UCP, and drain services for planned maintenance."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/workload-management-with-dynamic-database-services.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/ensuring-application-continuity.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RAC services and Application Continuity

**Goal:** apps see few errors during node failures and planned maintenance: services move, connections drain,
and in-flight work is replayed.

## Services for Application Continuity (AC)
Set `-failovertype TRANSACTION` and `-commit_outcome TRUE`. Related attributes from the Oracle RAC guide:
- `-replay_init_time`: seconds you allow replay to start (default 300).
- `-retention`: seconds commit outcome is kept (default 86400).
- `-failoverretry` (recommended 30) and `-failoverdelay` (recommended 10 seconds).
- `-notification TRUE` enables FAN for OCI and ODP.NET clients.
- `-rlbgoal SERVICE_TIME`, and `-clbgoal LONG` when using run-time load balancing.
- `-session_state` is `DYNAMIC` by default (almost all applications); `STATIC` only for diagnostic applications that
  change no session state.
```bash
srvctl add service -db racdb -service app2 -serverpool Srvpool1 \
  -failovertype TRANSACTION -commit_outcome TRUE -replay_init_time 1800 \
  -retention 86400 -notification TRUE -rlbgoal SERVICE_TIME -clbgoal LONG \
  -failoverretry 30 -failoverdelay 10
srvctl modify service -db racdb -service app1 -commit_outcome TRUE -retention 86400 -notification TRUE
```
The first form is for a policy-managed database (server pool). The `modify` form enables Transaction Guard only:
setting just `-commit_outcome TRUE` gives Transaction Guard without Application Continuity.
For an administrator-managed database use `-preferred` and `-available` instance lists (the guide's XA example:
`-preferred RAC01 -available RAC02,RAC03`); `srvctl relocate service` moves a service.

## Fast Application Notification (FAN) with UCP
Fast Connection Failover needs the Universal Connection Pool: create the pool and call
`setFastConnectionFailoverEnabled(true)`, with `ucp.jar` on the classpath. For remote ONS subscriptions find the
ports with `srvctl config nodeapps -onsonly` and pass them in `setONSConfiguration`, e.g.
`pds.setONSConfiguration("nodes=racnode1:6200,racnode2:6200");` (the port comes from that output; `ons.jar` must be on
the classpath).

## Planned maintenance (drain)
The service attributes `-drain_timeout` and `-stopoption` control how long sessions get to finish and what happens
to sessions that have not completed afterwards. Requests that complete and check back into the pool or close can
be directed to an unaffected location. Not all sessions check connections back in, so Oracle recommends always
setting `-drain_timeout`; after it expires the `-stopoption` is applied.
- `srvctl stop service` accepts `-stopoption` `TRANSACTIONAL` or `IMMEDIATE`; `srvctl stop database` accepts
  `NORMAL`, `TRANSACTIONAL`, `IMMEDIATE` or `ABORT`.
- Both can be defined on the service or given to `srvctl`, where the command line takes precedence.
- Documentation examples:
```bash
srvctl stop service -node racnode01 -drain_timeout 60 -stopoption IMMEDIATE
srvctl stop instance -node racnode01 -drain_timeout 60 -stopoption TRANSACTIONAL
srvctl relocate service -db mycdb01 -service myservice -drain_timeout 120 -stopoption IMMEDIATE -oldinst mycdb01_01 -force
```
`-force` is required when you give `-stopoption` to `relocate service` or `stop service` (and for a singleton
service or one not running on all nodes).

## Verify
- [ ] Each app connects to its own service via SCAN, never to an instance or SID.
- [ ] Kill a node in test: the application logs no errors and transactions complete once.
- [ ] A rolling restart with `-drain_timeout` shows connections moving, not erroring.

## Checked
2026-11-09. Read the 19c Oracle RAC Administration and Deployment Guide pages on dynamic database services
(`srvctl` service attributes and AC examples, FCF/UCP and ONS setup) and on ensuring application continuity (drain
timeout and stop options). Removed because they are not stated there: Transparent Application Continuity and
`-failovertype AUTO`, the `KEEP` grants, the replay-driver class and connect descriptor, the `acchk` /
`DBMS_APP_CONT_*` workflow and `GV$REPLAY_STAT_SUMMARY`, the claim that a service does not fail back, the
`-clbgoal SHORT` example (the guide says `LONG` with run-time load balancing) and the "separate OLTP and batch
services" advice.
Method: documentation only; no commands were run.
