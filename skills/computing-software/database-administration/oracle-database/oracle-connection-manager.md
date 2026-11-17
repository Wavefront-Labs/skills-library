---
id: computing-software.database-administration.oracle-database.oracle-connection-manager
name: oracle-connection-manager
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, connection-manager-cman, cman-ora, cmctl, oracle-net, proxy, access-control, traffic-director]
level: advanced
status: docs-checked
description: "Deploy Oracle Connection Manager (CMAN) as an Oracle Net proxy: cman.ora rules for access control, connection multiplexing, cmctl operations and client routing."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-oracle-connection-manager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle Connection Manager (CMAN)

CMAN is a proxy for Oracle Net: clients connect to CMAN, which forwards to database listeners.
Uses: single entry point through a firewall (open one port to CMAN instead of every DB host),
rule-based access control by client IP/service, session multiplexing, and Traffic Director mode (a proxy between supported OCI clients, 11.2 and later, and database instances).

## cman.ora
`$ORACLE_HOME/network/admin/cman.ora`:
```
cman_proxy =
  (CONFIGURATION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = cmanhost)(PORT = 1521))
    (RULE_LIST =
      (RULE = (SRC = 10.20.0.0/16)(DST = db01.corp.example.com)(SRV = app_svc)(ACT = accept)
        (ACTION_LIST = (AUT = off)(MCT = 0)(MIT = 0)))
      (RULE = (SRC = cmanhost)(DST = 127.0.0.1)(SRV = cmon)(ACT = accept))   -- needed for cmctl admin
      (RULE = (SRC = *)(DST = *)(SRV = *)(ACT = reject)))
    (PARAMETER_LIST =
      (MAX_GATEWAY_PROCESSES = 8)
      (VALID_NODE_CHECKING_REGISTRATION = on)
      (REGISTRATION_INVITED_NODES = (db01.corp.example.com))))
```
Rules match on source (SRC), destination host (DST) and service (SRV); the action (ACT: accept, reject or drop) of the first matching rule applies, and with no rules all connections are rejected. `ACTION_LIST` attributes (`AUT`, `MCT`, `MIT`) override defaults per connection; the documented example uses `MCT` and `MIT`, so check the parameter reference before using other abbreviations. CMCTL and CMAN must run on the same computer (the `cmon` rule).

## Operate
```bash
cmctl startup -c cman_proxy
cmctl show status -c cman_proxy
cmctl show services -c cman_proxy
cmctl show connections -c cman_proxy
cmctl reload -c cman_proxy        # re-read rules without dropping connections
cmctl shutdown -c cman_proxy
```

## Client side
Route through CMAN with source routing in the descriptor:
```
APP =
  (DESCRIPTION =
    (SOURCE_ROUTE = YES)
    (ADDRESS = (PROTOCOL = TCP)(HOST = cmanhost)(PORT = 1521))
    (ADDRESS = (PROTOCOL = TCP)(HOST = db01.corp.example.com)(PORT = 1521))
    (CONNECT_DATA = (SERVICE_NAME = app_svc)))
```
Alternatively, databases register with CMAN (`ALTER SYSTEM SET remote_listener = 'cmanhost:1521'`)
and clients connect to CMAN directly with the service name; CMAN routes to registered instances (load balances across RAC).

## Gotchas
- Without the `cmon` rule, `cmctl` cannot administer the instance.
- CMAN is a single point of failure: run two.
- Confirm licensing for your edition before deploying; Traffic Director mode has different terms from classic mode.

## Checked
2026-11-01. Confirmed on the 19c Net Services Administrator's Guide Connection Manager page: rule parameters SRC, DST, SRV, ACT and ACTION_LIST, first matching rule wins, no rules means all rejected, cmon rule and same-computer requirement, MAX_GATEWAY_PROCESSES, VALID_NODE_CHECKING and REGISTRATION_INVITED_NODES, REMOTE_LISTENER registration, Traffic Director OCI client note. Removed: MOCT (the documented attribute is MCT), CONN_STATS, MAX_CONNECTIONS, IDLE_TIMEOUT, INBOUND_CONNECT_TIMEOUT, LOG_LEVEL, log path, error numbers, TLS and failover claims, 18c version gate, dead cman.ora reference source.
Method: documentation only; no commands were run.

## Verify
A client from an allowed subnet connects via CMAN; one from a blocked subnet is refused by the rules; `cmctl show connections` lists the session.
