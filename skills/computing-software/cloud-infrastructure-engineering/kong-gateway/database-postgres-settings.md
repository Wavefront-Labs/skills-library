---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.database-postgres-settings
name: database-postgres-settings
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, pg-host, pg-user, postgres, kong-conf, database]
level: practitioner
status: docs-checked
description: "kong.conf pg_* settings for Kong's PostgreSQL datastore: host, port, user, database, timeouts, SSL, pool size and query limits with their defaults."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL connection settings

Set `database = postgres` (the default; `off` means DB-less). Connection options in `kong.conf`:

| Setting | Default |
|---|---|
| `pg_host` | `127.0.0.1` |
| `pg_port` | `5432` |
| `pg_user` | `kong` |
| `pg_password` | empty |
| `pg_database` | `kong` |
| `pg_schema` | unset (uses the server `search_path`) |
| `pg_timeout` | `5000` ms (connect, read, write) |
| `pg_ssl` | `off` |
| `pg_ssl_verify` | `off` (only meaningful when `pg_ssl` is on) |
| `pg_max_concurrent_queries` | `0` (unlimited per worker) |
| `pg_semaphore_timeout` | `60000` ms; failures generally make the request fail with HTTP 500 |
| `pg_pool_size` | falls back to `lua_socket_pool_size` (256) |
| `pg_keepalive_timeout` | falls back to `lua_socket_keepalive_timeout` |
| `pg_backlog` | unset (open connections not limited); if set, queue size for waiters when the pool is full |

Each setting can also be an environment variable named with the `KONG_` prefix and the uppercase setting name.

`pg_ssl` is only a hint: PostgreSQL uses the same port for TLS and non-TLS, so if the server does not support TLS the connection will be a plain one. `pg_ssl_verify` uses the CA set by `lua_ssl_trusted_certificate`.

## Checked

2026-11-04. Confirmed against kong.conf.default: `database` values, every default in the table, the per-worker note on `pg_max_concurrent_queries` and `pg_pool_size`, `lua_socket_pool_size` 256, the `pg_ssl` hint behaviour. Removed the `KONG_PG_PASSWORD` and vault advice and the "enable verify to enforce" claim, which the page does not state.
Method: documentation only; no commands were run.
