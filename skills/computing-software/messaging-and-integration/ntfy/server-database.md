---
id: computing-software.messaging-and-integration.ntfy.server-database
name: server-database
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, database, postgresql, sqlite, database-url]
level: advanced
status: docs-checked
description: "Choose between ntfy's default SQLite files and PostgreSQL via database-url, with replicas, pool settings and access-control side effects."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Database options

ntfy stores the message cache, users and access control, and web push subscriptions.

## SQLite (default)

Separate files: `cache-file`, `auth-file` (setting it enables auth) and `web-push-file`.

## PostgreSQL

```yaml
database-url: "postgres://user:pass@host:5432/ntfy"
```

Also `NTFY_DATABASE_URL` or `--database-url`. When set, `cache-file`, `auth-file` and `web-push-file` must not be set.

## Gotchas

- `database-url` implicitly enables authentication and access control, but default access stays `read-write`, so anonymous users can still read and write. Set `auth-default-access: "deny-all"` to restrict.
- Read replicas: `database-replica-urls` (env `NTFY_DATABASE_REPLICA_URLS`, comma-separated). Non-critical reads go to the replica with the fewest connections in use; writes and correctness-critical reads go to the primary; if every replica is unhealthy ntfy falls back to the primary.
- Pool parameters are URL query params: `pool_max_conns` (default 10), `pool_max_idle_conns`, `pool_conn_max_lifetime`, `pool_conn_max_idle_time`. Suggested for busy servers: `pool_max_conns=30&pool_conn_max_lifetime=15m&pool_conn_max_idle_time=5m`.
- PostgreSQL `max_connections` must cover pool size times ntfy instances plus other clients.
- Servers sharing a database need synced clocks (daily limits use each server's clock).

## Monitoring

Watch `ntfy_db_pool_waits_total` (waits that keep rising mean the pool is too small) and alert on `ntfy_db_up{role="primary"} == 0`.

## Checked

2026-11-04. Confirmed against the ntfy config page (Database options: SQLite files, PostgreSQL, replicas, pool parameters and defaults, recommended pool settings, metrics). Corrected: replica selection is by fewest connections, not plain round-robin.
Method: documentation only; no commands were run.
