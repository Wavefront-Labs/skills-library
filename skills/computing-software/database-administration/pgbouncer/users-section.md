---
id: computing-software.database-administration.pgbouncer.users-section
name: users-section
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, users-section, per-user, pool-size, timeouts]
level: practitioner
status: docs-checked
description: "The [users] section: per-user overrides for pool_size, pool_mode, timeouts and connection limits, and its interaction with auth_file and auth_user."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: apply settings to individual users.

Lines are `user1 = key=value ...`, for example `user1 = pool_mode=session`. Only a few settings are available:

- `pool_size`: maximum pool size for all connections from this user; otherwise the database or default_pool_size applies.
- `reserve_pool_size`: extra connections for this user; otherwise the database or global value.
- `pool_mode`: for all connections from the user; otherwise the database or default mode.
- `max_user_connections`: server connections for this user across all pools.
- `max_user_client_connections`: client connections for this user, the user equivalent of max_client_conn.
- `query_timeout`, `query_wait_timeout` (-1 means not set), `idle_transaction_timeout`, `transaction_timeout`, `client_idle_timeout`: override the server-level values. The docs flag client_idle_timeout as potentially dangerous.

```
[users]
reporting = pool_mode=session pool_size=5 query_timeout=600
```

If auth_file is configured and a user is defined here but not in auth_file, PgBouncer tries auth_query to find a password if auth_user is set. If auth_user is not set, PgBouncer behaves as if the user exists (no "no such user" message goes to the client) but accepts no provided password.

SHOW USERS reports each override (NULL if not set), current_connections and current_client_connections.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
