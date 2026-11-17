---
id: computing-software.database-administration.oracle-database.listener-configuration-and-lsnrctl
name: listener-configuration-and-lsnrctl
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-net, listener, lsnrctl, listener-ora, valid-node-checking, scan-listener]
level: practitioner
status: docs-checked
description: "Configure the Oracle listener (dynamic registration, valid nodes) and run lsnrctl to start, stop, reload, list services and set logging."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netag/configuring-and-administering-oracle-net-listener.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/netrf/listener-control-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Listener configuration and lsnrctl

## What the listener is
- Its configuration lives in `listener.ora`. All parameters have defaults, so a listener can start with no
  configuration: it is named `LISTENER`, supports no services at startup and listens on
  `(ADDRESS=(PROTOCOL=tcp)(HOST=host_name)(PORT=1521))`.
- The listener release must be the same as or later than every database it serves.
- Services normally register themselves (dynamic registration) through the LREG process; this needs no `listener.ora`
  entries. It supports connect-time failover and connection load balancing.

## Dynamic registration
- Initialization parameters involved: `SERVICE_NAMES`, `INSTANCE_NAME`, `LOCAL_LISTENER`, `REMOTE_LISTENER`,
  `FORWARD_LISTENER`. `SERVICE_NAMES` defaults to `DB_NAME` plus `DB_DOMAIN` and `INSTANCE_NAME` to the SID. From 19c
  customer use of `SERVICE_NAMES` is deprecated; manage services with `SRVCTL`, `GDSCTL` or `DBMS_SERVICE`.
- By default LREG registers with the local listener on TCP port 1521. For another address set `LOCAL_LISTENER`
  (`ALTER SYSTEM SET LOCAL_LISTENER=listener_sales1;`, alias resolved through `tnsnames.ora` on the database host). An
  invalid or unresolvable alias stops the database from starting.
- In a dedicated server environment, registering with a remote listener needs `REMOTE_LISTENER`.
- The listener must listen on the ports named in the initialization file and must not have parameters such as COST
  that prevent automatic registration.

## Restrict who can register
- By default registration connections are filtered by IP: only the local machine is allowed. If you specify nodes or
  subnets, the local machine plus those are allowed.
- `listener.ora` parameters: `REGISTRATION_INVITED_NODES_<listener_name>` (hosts or CIDR addresses that may register)
  and `REGISTRATION_EXCLUDED_NODES_<listener_name>` (ignored if both are set); `VALID_NODE_CHECKING_REGISTRATION_<listener_name>`.
- With Grid Infrastructure, for a SCAN listener the listener agent overwrites these parameters. Setting invited nodes
  and subnets with `srvctl` makes the agent set `VALID_NODE_CHECKING_REGISTRATION` to `SUBNET`. `srvctl` cannot set
  invited nodes for a non-SCAN listener.

## lsnrctl
Syntax is `lsnrctl <command> [listener_name]`; without a name the command goes to `LISTENER`. Commands can also be
typed at the `LSNRCTL>` prompt or run from a file (`lsnrctl @file_name`, comments start with `REM` or `#`).
```bash
lsnrctl start [listener_name]
lsnrctl stop [listener_name]
lsnrctl status [listener_name]
lsnrctl services [listener_name]   # services, instances and handlers (dispatchers, dedicated servers)
lsnrctl reload                     # re-read listener.ora without stopping the listener
lsnrctl set log_status on          # turn listener logging on or off
```
- `status READY` appears in `SERVICES` output for registered instances.
- `RELOAD` lets you add or change statically configured services without stopping the listener; `RELOAD -with_ha`
  also keeps existing registrations.
- `SET` changes last until the listener shuts down; `SAVE_CONFIG` writes them to `listener.ora` (and first backs up
  the file as `listener.bak`).
- `lsnrctl` finds the listener name via `listener.ora` in `TNS_ADMIN`, then in `ORACLE_HOME/network/admin`, then a
  naming method such as `tnsnames.ora`; otherwise it assumes `LISTENER`, local host, port 1521.
- Remote administration can run every command except `START`. Local administration is limited by OS authentication to
  the account that started the listener (or superuser), and remote administration is disabled by default; Oracle
  recommends logging in to the host (for example by SSH) instead.
- Default log directory is `ORACLE_HOME/network/log` and the default log file name is `listener.log`; both can be
  changed with `SET LOG_DIRECTORY` and `SET LOG_FILE`.
- Under Oracle Restart or Grid Infrastructure use `srvctl start listener`, `srvctl stop listener` and
  `srvctl config listener` (add `-listener <name>`).

## Verify
`lsnrctl status` and `lsnrctl services` show the expected endpoints and services, and registration is limited to
intended nodes.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Net Services Administrator's Guide chapter "Configuring and
Administering Oracle Net Listener" (overview, dynamic registration, valid nodes, start/stop and SRVCTL sections read)
and the Net Services Reference chapter "Listener Control Utility" (overview, security, RELOAD, SERVICES, SET and
SAVE_CONFIG sections read; other commands skimmed). Removed (not on those pages): the sample `listener.ora`, static
`SID_LIST` and Data Guard `_DGMGRL` advice, `UNKNOWN` and `BLOCKED` status meanings, the ORA-/TNS- error map, log path
under ADR, log rotation steps, `ADMIN_RESTRICTIONS`, listener password remark, `TCP.INVITED_NODES` in sqlnet.ora.
Method: documentation only; no commands were run.
