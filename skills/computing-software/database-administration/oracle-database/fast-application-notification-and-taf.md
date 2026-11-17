---
id: computing-software.database-administration.oracle-database.fast-application-notification-and-taf
name: fast-application-notification-and-taf
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, fast-application-notification, taf, transparent-application-failover, ons, fan, failover-type, oci-clients]
level: advanced
status: draft
description: "Configure Oracle FAN (ONS events to pools) and TAF (failover of SELECTs for OCI clients) for RAC and Data Guard services, and test that clients actually react."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/ensuring-application-continuity.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-transparent-application-failover.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/racad/workload-management-with-dynamic-database-services.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast Application Notification and TAF

## FAN
Clusterware publishes UP/DOWN/planned events for services, instances and nodes through ONS
(Oracle Notification Service, port 6200 by default). FAN-aware clients:
- Clean up connections to a failed instance **immediately** instead of waiting for TCP timeouts (minutes).
- Drain connections gracefully on planned maintenance (`srvctl stop service ... -drain_timeout`).
- Rebalance with load advisory (runtime connection load balancing).
FAN-aware clients: JDBC with UCP (`ons.jar`, `simplefan.jar`), ODP.NET managed/unmanaged (`HA events=true`), OCI/OCCI with
`events = true` in `oraaccess.xml` or service with `-notification TRUE`, WebLogic Active GridLink, Tuxedo.
Since 12.2, clients auto-configure ONS from the connect string; firewall must allow the client to reach port 6200 on all nodes.
```bash
srvctl config nodeapps -onsonly
srvctl status ons
```
Watch events (test): set a callout script in `$GRID_HOME/racg/usrco/` that logs its arguments, then stop an instance.

## TAF (OCI-based clients)
TAF reconnects a session to a surviving instance and, with `SELECT` type, replays the open query
and skips rows already fetched. It does **not** replay transactions: in-flight DML gets ORA-25402 and must be rolled back and retried by the application.
Server-side (preferred; clients need nothing in tnsnames):
```bash
srvctl add service -db ORCL -service app_taf -preferred ORCL1,ORCL2 \
  -failovertype SELECT -failovermethod BASIC -failoverretry 30 -failoverdelay 5 -notification TRUE
srvctl start service -db ORCL -service app_taf
```
Client-side alternative:
```
APP_TAF = (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = rac-scan)(PORT = 1521))
  (CONNECT_DATA = (SERVICE_NAME = app_taf)
    (FAILOVER_MODE = (TYPE = SELECT)(METHOD = BASIC)(RETRIES = 30)(DELAY = 5))))
```
Check it is active per session:
```sql
SELECT inst_id, username, service_name, failover_type, failover_method, failed_over FROM gv$session WHERE username = 'APPUSER';
```
JDBC thin does not support TAF: use Application Continuity (`-failovertype TRANSACTION` or `AUTO` for TAC) with UCP.

## Choosing
| Client | Use |
|---|---|
| Java/.NET with pools | FAN + (Transparent) Application Continuity |
| OCI tools, reporting (SQL*Plus, C apps) | TAF SELECT + FAN |
| Any client | at minimum FAN or short TCP timeouts so dead connections are detected |

## Gotchas
- TAF with `METHOD = PRECONNECT` holds a shadow session on the backup instance (resource cost).
- Session state (ALTER SESSION, PL/SQL package state, temp tables) is lost on TAF failover; apps must re-establish it (TAF callback).
- FAN requires the service to be used for connections; connecting via SID bypasses it.

## Verify
Kill an instance (`srvctl stop instance -stopoption abort` in test): a long SELECT in SQL*Plus over `app_taf` continues and `failed_over = YES`; pooled apps log FAN DOWN events and recover in seconds.
