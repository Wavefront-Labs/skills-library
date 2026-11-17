---
id: computing-software.database-administration.pgbouncer.pool-sizing-settings
name: pool-sizing-settings
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, pool-size, default-pool-size, min-pool-size, reserve-pool]
level: practitioner
status: docs-checked
description: "default_pool_size, min_pool_size, reserve_pool_size and reserve_pool_timeout: defaults, scope and per-database and per-user overrides."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size server-connection pools per user/database pair.

- `default_pool_size` (default 20): maximum server connections per user/database pair. Overridden by `pool_size` in a [databases] entry or a [users] entry.
- `min_pool_size` (default 0, disabled): add server connections when the pool is below this number, which helps when normal load suddenly returns after total inactivity. Effectively capped at the pool size. It is enforced only for pools where the [databases] entry has a user key (forced user) or at least one client is connected. Can be set per database.
- `reserve_pool_size` (default 0, disabled): extra connections allowed to a pool. Overridable per database and per user; `reserve_pool` is a backward-compatible alias in [databases].
- `reserve_pool_timeout` (default 5.0 seconds): if a client has not been serviced in this time, the reserve pool is used. 0 disables.

A pool exists for each (database, user) couple. If a [databases] entry sets `user=`, all connections use that user, so there is only one pool for that database; otherwise PgBouncer logs in as the client user and there is one pool per user.

Precedence for pool_size: user setting, else database setting, else default_pool_size.

```
[databases]
app = host=db1 pool_size=40 min_pool_size=5 reserve_pool_size=5
[users]
etl = pool_size=10
```

Watch SHOW POOLS: if maxwait keeps increasing, the pool is too small or the server is overloaded.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
