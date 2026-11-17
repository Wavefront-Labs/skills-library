---
id: computing-software.database-administration.pgbouncer.connection-limits
name: connection-limits
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, max-client-conn, max-db-connections, max-user-connections, limits]
level: practitioner
status: docs-checked
description: "max_client_conn, max_db_connections, max_user_connections and their client-side variants: defaults and how they interact."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cap connections globally, per database and per user.

- `max_client_conn` (default 100): maximum client connections PgBouncer accepts.
- `max_db_connections` (default 0, unlimited): server connections per PgBouncer database regardless of user. It counts the PgBouncer database the client connected to, not the PostgreSQL database of the outgoing connection. Also settable per database.
- `max_db_client_connections` (default 0, unlimited): client connections per database. Should be at least max_db_connections; the difference is how many can queue while waiting. Also per database.
- `max_user_connections` (default 0, unlimited): server connections per user regardless of database. It counts the user associated with the pool: the forced server user if there is one, else the client user. Also per user in [users].
- `max_user_client_connections` (default 0, unlimited): client connections per user. Set it higher than max_user_connections; the difference is the user's queue size. Also per user.

When a per-database or per-user server limit is reached, closing a client in one pool does not immediately free a server connection for another pool. The first pool's server connection stays open until it closes (idle timeout); then a new one is opened immediately for the waiting pool.

Raising max_client_conn may require raising OS file descriptor limits (ulimit). The theoretical file descriptor use is max_client_conn + (max pool_size * total databases * total users), or without the users factor if all users share one database user. Windows has no ulimit.

SHOW DATABASES and SHOW USERS display the effective limits and current counts.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
