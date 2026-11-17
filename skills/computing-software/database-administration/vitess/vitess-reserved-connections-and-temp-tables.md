---
id: computing-software.database-administration.vitess.vitess-reserved-connections-and-temp-tables
name: vitess-reserved-connections-and-temp-tables
category: computing-software
field: database-administration
product: vitess
tags: [reserved-connections, temporary-tables, connection-pool, get-lock, vtgate, keepalive]
level: advanced
status: docs-checked
description: "Know when Vitess pins a MySQL connection to a session: temporary tables and GET_LOCK, why SET no longer does, and the temp-table keepalive and idle-timeout flags."
sources:
  - https://vitess.io/docs/25.0/reference/query-serving/reserved-conn/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitess pools connections so many client sessions share few MySQL connections, and rewrites state-changing constructs such as user variables so state stays in vtgate. When that is not enough it uses a reserved connection: a dedicated vttablet-to-MySQL connection for the vtgate session. Use them sparingly, since they reduce pooling effectiveness. `SET` statements no longer cause reserved connections; the pool tracks connections with modified settings instead. Still reserved: temporary tables (until the client disconnects; dropping the table is not enough) and locking functions such as `GET_LOCK()`, whose connection is also kept alive. Each time a connection becomes reserved a fresh one replaces it in the pool.

Temp-table keepalive: vtgate sends a low-frequency heartbeat that refreshes only the tablet's own timers and sends nothing to mysqld, so MySQL `wait_timeout` still ends an idle session and its temp tables. `--temp-table-heartbeat-time` on VTGate (duration, default `10s`) sets the interval for MySQL-protocol sessions; `0` disables it and falls back to reclaiming at the transaction timeout.

gRPC sessions have no wire connection to anchor a heartbeat, so `--queryserver-config-temp-table-idle-timeout` on VTTablet (default `-1`) applies: `-1` mirrors `@@global.wait_timeout`, `0` reclaims at the transaction timeout, and a positive value sets an explicit timeout (keep it at or above the transaction timeout and at or below `wait_timeout`). Warning from the page: with `-1`, an abandoned gRPC session can linger up to `wait_timeout` (8h by default) instead of the 30s transaction timeout, occupying the stateful pool.

Metrics: `TempTableUnmanagedConnections` (gauge) and `TempTableIdleTimeoutKills` (counter). Upgrade vttablets before vtgates.

## Checked

2026-11-04. Reserved connection triggers, keepalive and idle-timeout flags, warning and metrics confirmed on the Reserved Connections page.

Method: documentation only; no commands were run.
