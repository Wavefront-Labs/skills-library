---
id: computing-software.database-administration.vitess.vttablet-connection-pools
name: vttablet-connection-pools
category: computing-software
field: database-administration
product: vitess
tags: [connection-pooling, vttablet, mysql-connections, capacity, metrics]
level: advanced
status: docs-checked
description: "Size and diagnose VTTablet MySQL connection pools: each pool flag and default, the _active and _exhausted metrics, and the formula for maximum connections per tablet."
sources:
  - https://vitess.io/docs/25.0/reference/features/connection-pools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VTTablet connects to mysqld through several pools that grow on demand to their maximum and in current versions effectively never shrink. Pools do not use unique MySQL usernames, so use metrics, not the process list, to see usage: `vttablet_dba_conn_pool_active` shows connections in use and `vttablet_dba_conn_pool_exhausted` counts times a pool ran out. Exhaustion is not necessarily bad, since it limits database concurrency; size pools to MySQL capacity.

Pools and flags (defaults):
- transaction pool and found-rows pool: `--queryserver-config-transaction-cap` (20) for each.
- conn pool (normal queries): `--queryserver-config-pool-size` (16).
- stream pool: `--queryserver-config-stream-pool-size` (200).
- dba pool (`ExecuteFetchAsDBA`, schema reloads): `--dba-pool-size` (20).
- app pool (`ExecuteFetchAsApp`): `--app-pool-size` (40).
- tx-read pool: hardcoded 3, used only with TWOPC. Online DDL executor pool: hardcoded 3. Table GC pool: 2.

Approximate maximum connections per tablet: transaction-cap x 2, plus pool-size, stream-pool-size, dba-pool-size, app-pool-size, plus 3 (tx-read), 7 (online DDL), and a variable amount (under 10) for VReplication and MySQL replication, plus reserved connections for `enable_system_settings`. Most servers will use far fewer.

Per-user limit: `--transaction-limit-per-user` (0.4) applies only if `--enable-transaction-limit` is set; `--transaction-limit-by-username` defaults to true. On VTGate, `--denied-system-variables=unique_checks,sql_log_off` blocks listed SETs with error 1235 (VT12001); changes need a VTGate restart.

## Checked

2026-11-04. Pool flags, defaults, metric names, the connection formula and the denied-system-variables example confirmed on the Connection Pools page.

Method: documentation only; no commands were run.
