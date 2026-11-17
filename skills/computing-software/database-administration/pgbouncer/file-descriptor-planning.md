---
id: computing-software.database-administration.pgbouncer.file-descriptor-planning
name: file-descriptor-planning
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, file-descriptors, ulimit, max-client-conn, capacity]
level: practitioner
status: docs-checked
description: "Estimate the file descriptors PgBouncer can use from max_client_conn and pool sizes and raise ulimit accordingly."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid hitting OS descriptor limits.

When max_client_conn (default 100) is raised, the OS file descriptor limit may also need raising. The number of descriptors that can be used is more than max_client_conn. The docs give the theoretical maximum:

- If each user connects under its own user name: `max_client_conn + (max pool_size * total databases * total users)`.
- If a database user is specified in the connection string (all users connect as the same user): `max_client_conn + (max pool_size * total databases)`.

Worked example: max_client_conn=1000, pool_size 20, 2 databases, forced user: 1000 + (20 * 2) = 1040. With 5 users and no forced user: 1000 + (20 * 2 * 5) = 1200.

The docs say the theoretical maximum should never be reached unless someone deliberately crafts a load for it, but you should still set the descriptor limit to a safely high number. Search your shell's man page for `ulimit`. ulimit does not apply on Windows.

Related caps: default_pool_size (20), max_db_connections and max_user_connections (both 0, unlimited, by default) bound the server-side term. Listening backlog is a separate setting, listen_backlog (128).

```
ulimit -n 4096
pgbouncer -d /path/to/pgbouncer.ini
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an unconfirmed claim that SHOW LISTS and SHOW SOCKETS help observe descriptor usage.

Method: documentation only; no commands were run.
