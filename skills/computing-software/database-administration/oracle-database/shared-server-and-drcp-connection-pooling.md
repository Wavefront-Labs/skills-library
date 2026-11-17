---
id: computing-software.database-administration.oracle-database.shared-server-and-drcp-connection-pooling
name: shared-server-and-drcp-connection-pooling
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, shared-server, drcp, database-resident-connection-pooling, dispatchers, connection-pooling, oracle-net]
level: advanced
status: docs-checked
description: "Cut Oracle server process count with shared server (dispatchers) or Database Resident Connection Pooling (DRCP): compare, configure, monitor."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/managing-processes.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/jjdbc/database-resident-connection-pooling.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_CONNECTION_POOL.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared server and DRCP

A dedicated server is one server process per user process. Many mostly idle connections waste server resources, and
two server-side options reduce that. Dedicated connections are always allowed; shared server and DRCP must be
enabled.

## Compared (Administrator's Guide table 5-1)
| | Dedicated | Shared server | DRCP |
|---|---|---|---|
| Request handling | new server process and session per client | dispatcher puts request on a common queue; an available shared server picks it up | connection broker hands the connection to an available pooled server, creates one if none, or queues the request if the pool is at maximum size |
| Session memory | PGA | SGA | PGA |
| Memory scales with | server processes and sessions (one each per client) | shared servers plus sessions (one session per client) | pooled servers and their sessions; each broker connection costs about 35 KB |

Worked example in the guide (400 KB per session, 4 MB per server process, 5000 clients, pool of 100): about 22 GB
dedicated, 2.5 GB shared server, 615 MB DRCP.

## Shared server
- Enabled by setting `SHARED_SERVERS` above 0; it is the only required parameter and sets the initial and minimum
  number of shared servers. Set it to 0 to disable (dynamic with `ALTER SYSTEM`).
- If `DISPATCHERS` is unset, enabling shared server creates one TCP dispatcher. At least one dispatcher is required.
  The number of dispatchers does not adjust automatically; change it with `ALTER SYSTEM`.
- `MAX_SHARED_SERVERS` caps the number PMON creates automatically (no default). `SHARED_SERVERS` overrides it if
  higher. `SHARED_SERVER_SESSIONS` limits shared-server sessions so some can be reserved for dedicated servers, so
  backup and recovery are not preempted.
- Shared server needs UGA space in the shared pool or large pool; tune memory when expecting many sessions.
```sql
ALTER SYSTEM SET shared_servers = 5;
ALTER SYSTEM SET dispatchers = '(PROTOCOL=TCP)(DISPATCHERS=2)';
```
- Connect with a dedicated server (net service name with `SERVER=DEDICATED` in the connect descriptor) for batch jobs
  and for RMAN backup, restore or recovery.
- Views: `V$DISPATCHER`, `V$DISPATCHER_CONFIG`, `V$DISPATCHER_RATE`, `V$QUEUE`, `V$SHARED_SERVER`, `V$CIRCUIT`,
  `V$SHARED_SERVER_MONITOR`.

## DRCP
- `SYS_DEFAULT_CONNECTION_POOL` exists but is not started by default. Start it as SYS:
  `EXECUTE DBMS_CONNECTION_POOL.START_POOL();`. It stays started until stopped and restarts with the instance if it
  was active at shutdown. Stop it with `STOP_POOL`; this completes only after requests already handed to a server
  finish. In RAC any instance can manage the pool and changes apply to all instances.
- Route clients to it with `POOLED` in the connect string: `host:1521/service:POOLED` (easy connect), or
  `(CONNECT_DATA=(SERVICE_NAME=sales)(SERVER=POOLED))`. Only TCP is supported.
- JDBC: set a non-empty `oracle.jdbc.DRCPConnectionClass` property and use `(SERVER=POOLED)` or the `:POOLED` short
  URL. Pooled servers are shared across client pools that use the same connection class. DRCP benefits come from a
  client-side pool; JDBC has no default pool of its own.
- Configure with `DBMS_CONNECTION_POOL.CONFIGURE_POOL` (all parameters) or `ALTER_PARAM` (one). `RESTORE_DEFAULTS`
  resets. Only the default pool name is supported.

| Parameter | Default | Meaning |
|---|---|---|
| `MINSIZE` | 4 | minimum pooled servers |
| `MAXSIZE` | 40 | maximum pooled servers; 5% (at least one) are reserved for authentication |
| `INCRSIZE` | 2 | servers added when none are available |
| `SESSION_CACHED_CURSORS` | 20 | cursors cached per pooled session |
| `INACTIVITY_TIMEOUT` | 300 s | idle pooled server is terminated (not applied at `MINSIZE`) |
| `MAX_THINK_TIME` | 120 s | client idle after obtaining a server: server is freed and the client connection ends, so later calls can raise ORA-3113 or ORA-3115 |
| `MAX_TXN_THINK_TIME` | = `MAX_THINK_TIME` | same, for clients with an open transaction |
| `MAX_USE_SESSION` | 500000 | take-and-release cycles before a server is replaced (0 disables) |
| `MAX_LIFETIME_SESSION` | 86400 s | lifetime of a pooled server (0 disables) |
| `NUM_CBROK`, `MAXCONN_CBROK` | 1, 40000 | connection brokers, and connections per broker (raise the OS file descriptor limit to match) |

- `MIN_AUTH_SERVERS` and `MAX_AUTH_SERVERS` size the separate authentication pool. `DRCP_DEDICATED_OPT = Yes` makes
  DRCP behave like a dedicated server while connections to the broker are below the pool maximum.
- Views: `DBA_CPOOL_INFO`, `V$CPOOL_CONN_INFO` (state of each broker connection), `V$CPOOL_STATS`,
  `V$CPOOL_CC_INFO`, `V$CPOOL_CC_STATS`.

## Verify
`DBA_CPOOL_INFO` shows the pool started, clients connect with `POOLED` and a connection class, and batch and RMAN
connections use `SERVER=DEDICATED` when shared server is on.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Administrator's Guide chapter "Managing Processes" (sections 5.1,
5.2, 5.4 and 5.5 read; table 5-1 and 5-2 values quoted), the JDBC Developer's Guide chapter "Database Resident
Connection Pooling" (read in full) and the PL/SQL Packages reference page DBMS_CONNECTION_POOL (read in full).
Removed (not on those pages): sample `shared_servers`/`large_pool_size` figures, `(SERVICE=...)` dispatcher advice,
`SERVER=SHARED` client setting, v$ monitoring queries with column lists and thresholds, "11g+" and 21c per-PDB pool
statements, purity NEW/SELF behaviour, ORA-04031 advice, `lsnrctl services` remark, and the "which one" chooser table.
Method: documentation only; no commands were run.
