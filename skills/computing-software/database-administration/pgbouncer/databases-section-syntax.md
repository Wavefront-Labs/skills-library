---
id: computing-software.database-administration.pgbouncer.databases-section-syntax
name: databases-section-syntax
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, databases-section, connection-string, dbname, forced-user]
level: practitioner
status: docs-checked
description: "The [databases] section: key=value connection strings, quoting rules, the * fallback and per-entry parameters like dbname, host, port, user, password."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: map PgBouncer database names to PostgreSQL destinations.

Each line is `name = connection string` of key=value pairs (libpq-like, but libpq is not used and the feature set differs):

```
[databases]
foodb =
bardb = host=localhost dbname=bazdb
forcedb = host=localhost port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO
* = host=foo
```

Names may contain `_0-9A-Za-z` unquoted; others need SQL identifier quoting (double quotes, `""` for a literal quote). `pgbouncer` is reserved for the console and cannot be a key.

Core keys:

- `dbname`: destination database; default is the client-side database name.
- `host`: name or IP, resolved at connection time and cached per dns_max_ttl. Starts with `/` for a Unix socket path, `@` for abstract. Default not set, meaning a Unix socket.
- `port`: default 5432.
- `user`: if set, all connections to the destination use this user, giving one pool for the database; otherwise the client user name is used, one pool per user.
- `password`: if absent, the auth_file password for that user is used. Auth_query-style dynamic discovery is not supported here.

Per-database overrides: auth_user, auth_query, auth_dbname, pool_size, min_pool_size, reserve_pool_size, pool_mode, query_wait_timeout, max_db_connections, max_db_client_connections, server_lifetime, load_balance_hosts, connect_query, client_encoding, datestyle, timezone.

`*` is a fallback used when the exact name is missing. Run `connect_query` after each connection is established; errors from it are logged and otherwise ignored.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
