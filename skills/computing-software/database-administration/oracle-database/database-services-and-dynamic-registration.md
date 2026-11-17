---
id: computing-software.database-administration.oracle-database.database-services-and-dynamic-registration
name: database-services-and-dynamic-registration
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-net, listener, service-registration, dynamic-registration, local-listener, remote-listener, dbms-service, lreg]
level: practitioner
status: docs-checked
description: "Create Oracle database services with DBMS_SERVICE and fix dynamic registration via LOCAL_LISTENER and REMOTE_LISTENER."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-and-administering-oracle-net-listener.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_SERVICE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database services and dynamic registration

**Goal:** applications connect to named services, and the listener knows about them through dynamic registration.

## Service names
`SERVICE_NAMES` defaults to the global database name (`DB_NAME` plus `DB_DOMAIN`). Since 19c customer use of
`SERVICE_NAMES` is deprecated: Oracle recommends `SRVCTL` or `GDSCTL`, or the `DBMS_SERVICE` package, to manage
services.

## Create without clusterware: DBMS_SERVICE
```sql
-- in a PDB, connect to that PDB first
EXEC DBMS_SERVICE.CREATE_SERVICE(service_name => 'sales_rw', network_name => 'sales_rw.corp.local');
EXEC DBMS_SERVICE.START_SERVICE('sales_rw');
EXEC DBMS_SERVICE.STOP_SERVICE('sales_rw');
EXEC DBMS_SERVICE.DELETE_SERVICE('sales_rw');
```
- `CREATE_SERVICE` creates the service name in the data dictionary; `network_name` is the name used in SQL*Net
  connect descriptors. Oracle advises the parameter-array interface for service attributes (such as `failover_type`,
  `drain_timeout`, `stop_option`, `commit_outcome`, `clb_goal`).
- To use `DBMS_SERVICE` on a PDB in a single instance you must connect to that PDB first.
- `START_SERVICE` and `STOP_SERVICE` cannot be used when services are managed by Oracle Clusterware, Oracle
  Restart or Global Data Services. `START_SERVICE` has an optional `instance_name` (NULL = local instance;
  `DBMS_SERVICE.ALL_INSTANCES` for all).

## Dynamic registration
The Listener Registration (LREG) process registers services with the listener; no `listener.ora` service entries are
needed. By default it registers with the local listener on the default local TCP/IP address, port 1521.
- `LOCAL_LISTENER`: configure it so LREG registers with a local listener that does not use TCP/IP port 1521. It is a
  comma-delimited list; if an address contains a comma, enclose the whole string in double quotes.
  ```sql
  ALTER SYSTEM SET LOCAL_LISTENER=listener_sales1;   -- alias resolved via tnsnames.ora on the database host
  ```
- `REMOTE_LISTENER`: in a dedicated-server environment, LREG registers with a remote listener (for example on
  another node, for redirection) when this comma-delimited parameter is set.
  ```sql
  ALTER SYSTEM SET REMOTE_LISTENER=listener_sales2;
  ```
- The `LISTENER` attribute of `DISPATCHERS` overrides `LOCAL_LISTENER`/`REMOTE_LISTENER` for dispatcher
  registration (shared server).
- Listener and database configuration must be synchronized (protocol address in `listener.ora`, location in the
  parameter file) for LREG to register with a nondefault or remote listener.
- By default all listeners are cross-registered; `LISTENER_NETWORKS` can designate subsets (do not also list those
  listeners in `LOCAL_LISTENER`/`REMOTE_LISTENER`).

## Verify
- [ ] The listener's service list shows each service registered after a listener restart.
- [ ] Each application connects through its own service name, not the default one.

## Checked
2026-11-09. Read the 19c Net Services Administrator's Guide listener chapter (service registration, LREG,
`LOCAL_LISTENER`, `REMOTE_LISTENER`, `LISTENER_NETWORKS`) and the `DBMS_SERVICE` reference (package notes,
`CREATE_SERVICE`, `START_SERVICE`, `STOP_SERVICE` signatures and restrictions). Removed because the pages do not
state them: the `srvctl add service` examples and role-based service behaviour, `SAVE STATE` and the startup/role
change trigger, the 60-second registration interval, `ALTER SYSTEM REGISTER`, `lsnrctl services`/`v$active_services`
checks, error-diagnosis list and the default-service comparison. The sample names are illustrative.
Method: documentation only; no commands were run.
