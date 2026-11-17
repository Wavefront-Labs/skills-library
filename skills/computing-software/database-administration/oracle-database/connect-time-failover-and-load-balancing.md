---
id: computing-software.database-administration.oracle-database.connect-time-failover-and-load-balancing
name: connect-time-failover-and-load-balancing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-net, connect-time-failover, load-balance, tnsnames-ora, connect-descriptor]
level: practitioner
status: docs-checked
description: "Oracle connect descriptors that fail over between addresses and balance load: ADDRESS_LIST, FAILOVER, LOAD_BALANCE, timeouts and retries."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/enabling-advanced-features.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netrf/local-naming-parameters-in-tns-ora-file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connect-time failover and load balancing

## Descriptor with failover to a second address
```
SALES =
  (DESCRIPTION =
    (CONNECT_TIMEOUT = 5)(TRANSPORT_CONNECT_TIMEOUT = 3)(RETRY_COUNT = 3)(RETRY_DELAY = 2)
    (FAILOVER = ON)(LOAD_BALANCE = OFF)
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = site1-host)(PORT = 1521))
      (ADDRESS = (PROTOCOL = TCP)(HOST = site2-host)(PORT = 1521)))
    (CONNECT_DATA = (SERVICE_NAME = sales.example.com)))
```
- `FAILOVER = ON`: if the first address fails, Oracle Net tries a different one. `OFF` tries one address. Default
  is on for DESCRIPTION_LIST, DESCRIPTION and ADDRESS_LIST.
- `LOAD_BALANCE = OFF`: addresses are tried sequentially until one succeeds. `ON`: a random sequence, spreading
  clients over listeners. Default is on under DESCRIPTION_LIST, off under DESCRIPTION, ADDRESS_LIST and ADDRESS.
- Guide table: failover on only = try each address in order until one succeeds; load balance and failover both
  on = try each address randomly until one succeeds; load balance on only = try one address picked at random;
  both off (and `SOURCE_ROUTE` off) = only the first address.
- `CONNECT_TIMEOUT`: time allowed to establish an Oracle Net connection, a superset of the TCP connect time
  (it includes connecting to the instance providing the service). Unit defaults to seconds (`ms`, `sec`, `min`
  accepted). It applies to each ADDRESS in an ADDRESS_LIST and to each IP a host name resolves to; it is
  equivalent to, and overrides, `SQLNET.OUTBOUND_CONNECT_TIMEOUT`.
- `TRANSPORT_CONNECT_TIMEOUT`: same unit rules, default 60 sec, also per address; equivalent to, and overrides,
  `TCP.CONNECT_TIMEOUT`.
- `RETRY_COUNT`: how many times the address list is traversed before the attempt ends. `RETRY_DELAY`: seconds
  between retries. Put both under DESCRIPTION.
- `CONNECT_TIMEOUT`, `TRANSPORT_CONNECT_TIMEOUT`, `RETRY_COUNT`, `RETRY_DELAY`, `FAILOVER` and `LOAD_BALANCE` can
  also be set per DESCRIPTION inside a DESCRIPTION_LIST; each DESCRIPTION is traversed per its own retries.

## Gotchas
- A statically configured `GLOBAL_DBNAME` in the `SID_LIST_listener_name` section of listener.ora disables
  connect-time failover; do not set it.
- Connect-time failover is not Transparent Application Failover. TAF (`FAILOVER_MODE` in `CONNECT_DATA`) acts on
  an established connection; the guide recommends configuring failover on the connected service, which overrides
  client-side settings.
- Active transactions are rolled back by TAF, and server-side session state such as PL/SQL package state is lost.

## Verify
With the first address down, a connect using the service name reaches the second address within the configured
timeouts.

## Checked
2026-11-09. Read the Oracle Net Services Administrator's Guide (advanced features: connect-time failover and client
load balancing parameters and table) and the Net Services Reference (tnsnames.ora `FAILOVER`, `LOAD_BALANCE`,
`CONNECT_TIMEOUT`, `RETRY_COUNT`, `RETRY_DELAY`, `TRANSPORT_CONNECT_TIMEOUT`), both 19c. Removed because the pages do not
state them: the Data Guard primary/standby design with role-based `srvctl` services and startup trigger,
`ORA-12514` behaviour, the RAC/SCAN section and `-clbgoal`/`-rlbgoal`, Easy Connect Plus, JDBC URL notes and the
snapshot standby warning. The timeout and retry values in the sample are illustrative, not recommendations.
Method: documentation only; no commands were run.
