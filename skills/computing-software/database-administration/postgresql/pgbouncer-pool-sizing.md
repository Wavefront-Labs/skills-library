---
id: computing-software.database-administration.postgresql.pgbouncer-pool-sizing
name: pgbouncer-pool-sizing
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-connection-pooling, pgbouncer, pool-sizing, default-pool-size, max-client-conn, max-db-connections, reserve-pool, cl-waiting]
level: practitioner
status: docs-checked
description: "Size PgBouncer pools (default_pool_size, max_client_conn, max_db_connections, reserve_pool) from cores and workload, and read SHOW POOLS to tune them."
sources:
  - https://www.pgbouncer.org/config.html#pool-settings
  - https://www.pgbouncer.org/usage.html#show-pools
  - https://wiki.postgresql.org/wiki/Number_Of_Database_Connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer pool sizing

**Goal:** enough server connections to keep the database busy, few enough that it is not thrashing, and clients that queue briefly rather than fail.

## The knobs
| Setting | Meaning |
|---|---|
| `max_client_conn` | Maximum client connections (default 100); raise OS file-descriptor limits when increasing it |
| `default_pool_size` | Maximum server connections per user/database pair (default 20) |
| `min_pool_size` | Add server connections when below this (default 0, disabled; only enforced for some pools, see config.html) |
| `reserve_pool_size` / `reserve_pool_timeout` | Extra connections when a client has not been serviced within `reserve_pool_timeout` (default 5 s); `reserve_pool_size` default 0 (disabled) |
| `max_db_connections` / `max_user_connections` | Caps on server connections per database / per user across their pools (default 0 = unlimited) |
| `query_wait_timeout` | Client is disconnected if no server connection is assigned in this time (default 120 s; 0 disables) |

## Starting point
- Active connections the server handles well is a small multiple of its core count (judgement; the cited wiki page explains why too many connections hurt). Divide across pools; illustrative values for 3 app users on one database: `default_pool_size = 15`, `max_db_connections = 50`.
- Keep `sum of pools` below PostgreSQL `max_connections` minus superuser/replication/maintenance headroom.
- `max_client_conn` (default 100) can sit far above the pool sizes; surplus clients queue for server connections.
- Several PgBouncer processes (`so_reuseport = 1`) when one is CPU-bound (single-threaded).

## Tuning from SHOW POOLS
```
psql -p 6432 pgbouncer -c 'SHOW POOLS;'
 database | user | cl_active | cl_waiting | sv_active | sv_idle | sv_used | maxwait | pool_mode
```
- `cl_waiting > 0` and `maxwait` rising with `sv_active = pool size`: pool saturated. First check for long or idle-in-transaction sessions on the server, then grow the pool if the DB has headroom (CPU, waits).
- `sv_idle` large constantly: pool oversized; shrink or lower `server_idle_timeout`.
- DB CPU pegged while `cl_waiting` high: more connections will make it worse; fix queries.

## Gotchas
- Each distinct (db, user) gets its own pool; many users multiply server connections. Consolidate app users.
- Application-side pools in front of PgBouncer (HikariCP etc.) should be modest; let PgBouncer do the multiplexing.

## Verify
Under peak load `cl_waiting` returns to 0 within seconds, `maxwait` stays under target (e.g. <100 ms), and DB active sessions stay near the chosen pool size.

## Checked
2026-10-31. Confirmed on pgbouncer.org config.html: defaults and meaning of max_client_conn (100), default_pool_size (20), min_pool_size, reserve_pool_size (0), reserve_pool_timeout (5), max_db_connections and max_user_connections (0, unlimited), query_wait_timeout (120), so_reuseport and the single-threaded note; usage.html SHOW POOLS columns. Removed: the cores x 2 to 4 formula (the wiki page gives no such figure) and the 'idle sockets are cheap' claim. The <100 ms target is judgement.
Method: documentation only; no commands were run.
