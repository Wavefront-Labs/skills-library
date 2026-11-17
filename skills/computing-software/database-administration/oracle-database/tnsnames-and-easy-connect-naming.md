---
id: computing-software.database-administration.oracle-database.tnsnames-and-easy-connect-naming
name: tnsnames-and-easy-connect-naming
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-net, tnsnames-ora, easy-connect, ezconnect-plus, connect-descriptor, tns-admin, failover-address-list, tnsping, names-directory-path, ldap-naming]
level: practitioner
status: docs-checked
description: "Write Oracle tnsnames.ora entries with failover and timeouts, use Easy Connect Plus strings, control naming with sqlnet.ora, and debug name resolution."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-naming-methods.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netrf/local-naming-parameters-in-tns-ora-file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tnsnames.ora and Easy Connect naming

## Naming methods and lookup order
The client looks for `tnsnames.ora` in the directory named by `TNS_ADMIN`; if that is unset or the file is not there,
in `ORACLE_HOME/network/admin` (or the Oracle base home's `network/admin` for a read-only home).
On Windows a process with no `TNS_ADMIN` in its environment (a service, for example) falls back to a `TNS_ADMIN`
value in the registry. Check `TNS_ADMIN` first when it works for you but not for the app.

## tnsnames.ora entries
```
SALES =
  (DESCRIPTION =
    (CONNECT_TIMEOUT = 5)(TRANSPORT_CONNECT_TIMEOUT = 3)(RETRY_COUNT = 3)(RETRY_DELAY = 2)
    (ADDRESS_LIST =
      (LOAD_BALANCE = OFF)(FAILOVER = ON)
      (ADDRESS = (PROTOCOL = TCP)(HOST = prod-scan.corp.local)(PORT = 1521))
      (ADDRESS = (PROTOCOL = TCP)(HOST = dr-scan.corp.local)(PORT = 1521)))
    (CONNECT_DATA = (SERVICE_NAME = sales_rw.corp.local)))

SALES_RO =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCPS)(HOST = prod-scan.corp.local)(PORT = 2484))
    (SECURITY = (SSL_SERVER_DN_MATCH = YES))
    (CONNECT_DATA = (SERVICE_NAME = sales_ro.corp.local)))
```
- Use `SERVICE_NAME` in `CONNECT_DATA`.
- `LOAD_BALANCE` and `FAILOVER` are set per `ADDRESS_LIST`; `CONNECT_TIMEOUT` covers the whole connection to the instance (more than the TCP connect)
  and is equivalent to, and overrides, sqlnet.ora `SQLNET.OUTBOUND_CONNECT_TIMEOUT`; `RETRY_COUNT` is how many times the address list is traversed;
  `RETRY_DELAY` is seconds between retries.
- `IFILE = /path/common_tns.ora` includes a shared file (up to three levels of nesting).
- Newer Oracle documentation deprecates the `SSL_`-prefixed connect parameters (such as `SSL_SERVER_DN_MATCH`) in favour of `TLS_` ones
  (`TLS_SERVER_DN_MATCH`); if both are set the `SSL_` one is ignored.

## Easy Connect and Easy Connect Plus (19c+)
```
sqlplus app@//prod-scan.corp.local:1521/sales_rw.corp.local
sqlplus app@"tcps://prod-scan.corp.local:2484/sales_ro.corp.local?ssl_server_dn_match=on"
sqlplus app@"prod-scan1,prod-scan2:1521/sales_rw?connect_timeout=5&retry_count=3"
```
Syntax: `[[protocol:]//]host1{,host12}[:port1]{,host2:port2}[/[service_name][:server][/instance_name]][?parameter_name=value{&parameter_name=value}]`.
Plus (19c and later) adds multiple hosts, TCPS, and name-value pairs added as DESCRIPTION-level parameters, so many apps
need no tnsnames.ora or sqlnet.ora and no `TNS_ADMIN`. `server` is `dedicated`, `shared` or `pooled`.

## Debugging
Work out which `tnsnames.ora` the failing process actually reads, using the lookup order above, then check the alias and
the `SERVICE_NAME` in it. Test with a real login, not only a listener ping.

## Centralised naming
Distribute a single tnsnames.ora with config management, or use Easy Connect Plus strings in app config, which need no naming files.

## Verify
- [ ] Apps connect by service name; descriptors include timeouts.
- [ ] The app host resolves the alias from the intended `tnsnames.ora`.
- [ ] DR descriptors tested after a switchover.

## Checked
2026-10-31. Confirmed against Oracle Database 19 Net Services Administrator's Guide (naming methods) and Net Services Reference (tnsnames.ora parameters): tnsnames.ora lookup order and the Windows registry fallback, `IFILE` nesting, `CONNECT_TIMEOUT`, `TRANSPORT_CONNECT_TIMEOUT`, `RETRY_COUNT`, `RETRY_DELAY`, `LOAD_BALANCE`/`FAILOVER`, the Easy Connect Plus syntax and its 19c, TCPS and no-config properties, and the `SSL_` to `TLS_` parameter deprecation.
Removed as unconfirmed: the `NAMES.DIRECTORY_PATH` value, the Instant Client path, the SID and Data Guard role-service rationale, the JDBC URL, `tnsping`/`sqlplus -L`/client trace settings, the ORA-12154 explanation and LDAP naming details; `wallet_location` was dropped from the Easy Connect example.
Method: documentation only; no commands were run.
